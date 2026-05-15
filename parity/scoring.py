import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Any

# Import tenant configuration
try:
    from parity.tenant_config import TenantProfile
except ImportError:
    TenantProfile = Any  # type: ignore


@dataclass
class FunctionScore:
    name: str
    tenant: Optional[Any] = None  # TenantProfile
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
        """
        Cutover verdict based on readiness score and tenant-specific threshold.
        Uses tenant.parity_threshold_pct if available, otherwise defaults to 95%.
        """
        score = self.readiness_score
        threshold = self.tenant.parity_threshold_pct if self.tenant else 95.0
        
        if score >= threshold:
            return "SAFE_TO_CUT"
        elif score >= threshold - 15:
            return "CUT_WITH_MONITORING"
        elif score >= threshold - 35:
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
        result = {
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
        
        # Add tenant profile info if available
        if self.tenant:
            result["tenant_profile"] = {
                "tenant_id": self.tenant.tenant_id,
                "name": self.tenant.name,
                "tier": self.tenant.tier,
                "parity_threshold_pct": self.tenant.parity_threshold_pct,
                "fee_tolerance_usd": float(self.tenant.fee_tolerance_usd),
                "anomaly_sigma_threshold": self.tenant.anomaly_sigma_threshold,
            }
        
        return result


TX_TYPE_TO_FUNCTION = {
    "domestic": "Domestic Wire Transfer",
    "international": "International Wire Transfer",
    "scheduled": "Scheduled Payment",
    "wire_transfer": "High-Value Wire Transfer",
}


def score_results(results: list[dict], tenant: Optional[Any] = None) -> list[dict]:
    """
    Score parity results by function using tenant-specific thresholds.
    
    Args:
        results: List of parity comparison results
        tenant: Optional TenantProfile for tenant-specific scoring
    
    Returns:
        List of function score dicts
    """
    def make_score() -> FunctionScore:
        return FunctionScore(name="", tenant=tenant)
    
    buckets: dict[str, FunctionScore] = defaultdict(make_score)

    for r in results:
        tx_type = r["transaction_type"]
        func_name: str = TX_TYPE_TO_FUNCTION.get(tx_type, tx_type)  # type: ignore
        if buckets[func_name].name == "":
            buckets[func_name].name = func_name
        buckets[func_name].ingest(r)

    scores = []
    for score in buckets.values():
        score.finalise()
        scores.append(score.to_dict())

    scores.sort(key=lambda x: x["readiness_score"], reverse=True)
    return scores


def format_score_summary(scores: list[dict]) -> str:
    """
    Format a human-readable multi-line summary of function scores.

    Args:
        scores: List of score dicts as returned by score_results()

    Returns:
        Multi-line string summary for CLI output and logs
    """
    if not scores:
        return "No scores available."

    lines = ["=" * 70, "PARITY SCORE SUMMARY", "=" * 70]

    for s in scores:
        total = s['total_transactions']
        passing = round(total * s['parity_rate_pct'] / 100)
        lines.append(f"\n{s['function']}")
        lines.append("-" * 70)
        lines.append(f"  Verdict:         {s['verdict']}")
        lines.append(f"  Parity Rate:     {s['parity_rate_pct']}% ({passing}/{total} passing)")
        lines.append(f"  Readiness Score: {s['readiness_score']}")

        crit = s.get('critical_divergences', 0)
        high = s.get('high_divergences', 0)
        med = s.get('medium_divergences', 0)
        if crit or high or med:
            lines.append(f"  Divergences:     Critical={crit}, High={high}, Medium={med}")

    lines.append("=" * 70)
    return "\n".join(lines)
