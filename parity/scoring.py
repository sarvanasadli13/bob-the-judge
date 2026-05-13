import math
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class FunctionScore:
    name: str
    total: int = 0
    passing: int = 0
    high_severity: int = 0
    medium_severity: int = 0
    critical_severity: int = 0
    avg_fee_diff: float = 0.0
    avg_settled_diff: float = 0.0
    avg_latency_improvement_pct: float = 0.0
    _fee_diffs: list = field(default_factory=list, repr=False)
    _settled_diffs: list = field(default_factory=list, repr=False)
    _latency_improvements: list = field(default_factory=list, repr=False)
    _amounts: list = field(default_factory=list, repr=False)

    def ingest(self, result: dict):
        self.total += 1
        if result["parity"]:
            self.passing += 1
        for d in result["divergences"]:
            sev = d["severity"]
            if sev == "CRITICAL":
                self.critical_severity += 1
            elif sev == "HIGH":
                self.high_severity += 1
            else:
                self.medium_severity += 1
        self._fee_diffs.append(result["fee_diff"])
        self._settled_diffs.append(result["settled_diff"])
        self._latency_improvements.append(result["latency_improvement_pct"])
        self._amounts.append(result.get("amount", 0))

    def finalise(self):
        if self._fee_diffs:
            self.avg_fee_diff = round(sum(self._fee_diffs) / len(self._fee_diffs), 4)
        if self._settled_diffs:
            self.avg_settled_diff = round(sum(self._settled_diffs) / len(self._settled_diffs), 4)
        if self._latency_improvements:
            self.avg_latency_improvement_pct = round(
                sum(self._latency_improvements) / len(self._latency_improvements), 1
            )

    @property
    def parity_rate(self) -> float:
        return round(self.passing / self.total * 100, 1) if self.total else 0.0

    @property
    def readiness_score(self) -> float:
        if self.total == 0:
            return 0.0
        base = self.parity_rate
        penalty = (self.critical_severity * 15) + (self.high_severity * 5) + (self.medium_severity * 1)
        return max(0.0, round(base - penalty, 1))

    @property
    def confidence_interval(self) -> tuple[float, float]:
        """95% Wilson score confidence interval for parity rate."""
        if self.total == 0:
            return (0.0, 0.0)
        n = self.total
        p = self.passing / n
        z = 1.96
        denominator = 1 + z * z / n
        center = (p + z * z / (2 * n)) / denominator
        margin = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denominator
        lo = max(0.0, round((center - margin) * 100, 1))
        hi = min(100.0, round((center + margin) * 100, 1))
        return (lo, hi)

    @property
    def exposure_usd(self) -> float:
        """USD volume at risk in this sample (divergent transactions × amount)."""
        if self.total == 0:
            return 0.0
        divergence_rate = 1.0 - (self.passing / self.total)
        total_vol = sum(self._amounts)
        return round(divergence_rate * total_vol, 0)

    @property
    def verdict(self) -> str:
        score = self.readiness_score
        if score >= 95:
            return "SAFE_TO_CUT"
        elif score >= 80:
            return "CUT_WITH_MONITORING"
        elif score >= 60:
            return "HOLD_INVESTIGATE"
        else:
            return "DO_NOT_CUT"

    @property
    def verdict_color(self) -> str:
        return {
            "SAFE_TO_CUT": "#00C851",
            "CUT_WITH_MONITORING": "#FFBB33",
            "HOLD_INVESTIGATE": "#FF8800",
            "DO_NOT_CUT": "#FF4444",
        }[self.verdict]

    def to_dict(self) -> dict:
        ci_lo, ci_hi = self.confidence_interval
        return {
            "function": self.name,
            "total_transactions": self.total,
            "parity_rate_pct": self.parity_rate,
            "ci_low": ci_lo,
            "ci_high": ci_hi,
            "readiness_score": self.readiness_score,
            "verdict": self.verdict,
            "verdict_color": self.verdict_color,
            "critical_divergences": self.critical_severity,
            "high_divergences": self.high_severity,
            "medium_divergences": self.medium_severity,
            "avg_fee_diff_usd": self.avg_fee_diff,
            "avg_settled_diff_usd": self.avg_settled_diff,
            "avg_latency_improvement_pct": self.avg_latency_improvement_pct,
            "exposure_usd": self.exposure_usd,
        }


TX_TYPE_TO_FUNCTION = {
    "domestic": "Domestic Wire Transfer",
    "international": "International Wire Transfer",
    "scheduled": "Scheduled Payment",
    "wire_transfer": "High-Value Wire Transfer",
}


def score_results(results: list[dict]) -> list[dict]:
    buckets: dict[str, FunctionScore] = defaultdict(lambda: FunctionScore(name=""))

    for r in results:
        tx_type = r["transaction_type"]
        func_name = TX_TYPE_TO_FUNCTION.get(tx_type, tx_type)
        if buckets[func_name].name == "":
            buckets[func_name].name = func_name
        buckets[func_name].ingest(r)

    scores = []
    for score in buckets.values():
        score.finalise()
        scores.append(score.to_dict())

    scores.sort(key=lambda x: x["readiness_score"], reverse=True)
    return scores
