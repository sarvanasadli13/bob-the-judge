from decimal import Decimal, ROUND_HALF_UP
from services.models import TransactionType

FEE_TOLERANCE = Decimal("0.02")        # 2 cents — acceptable rounding diff
AMOUNT_TOLERANCE = Decimal("0.05")     # 5 cents on settled amount
LATENCY_THRESHOLD_MS = 5

REGULATION_MAP = {
    ("international", "fee"):            "PSD2 Art. 45 — FX Transparency",
    ("international", "processed_amount"): "PSD2 Art. 45 — Settlement Integrity",
    ("wire_transfer", "fee"):            "SWIFT gpi SLA — Fee Consistency",
    ("wire_transfer", "processed_amount"): "Basel III — Operational Risk Capital",
    ("domestic", "fee"):                 "PSD2 Art. 62 — Charges",
    ("domestic", "processed_amount"):    "PSD2 Art. 62 — Settlement",
    ("scheduled", "fee"):               "PSD2 Art. 62 — Charges",
}
STATUS_REGULATION = "PCI DSS 6.5 — Processing Integrity"


def _d(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def compare_pair(pair: dict) -> dict:
    payment = pair["payment"]
    legacy = pair["legacy"]
    modern = pair["modern"]
    tx_type = payment["transaction_type"]

    divergences = []

    # --- fee comparison ---
    legacy_fee = _d(legacy.get("fee", 0))
    modern_fee = _d(modern.get("fee", 0))
    fee_diff = abs(legacy_fee - modern_fee)
    fee_match = fee_diff <= FEE_TOLERANCE

    if not fee_match:
        divergences.append({
            "field": "fee",
            "legacy": float(legacy_fee),
            "modern": float(modern_fee),
            "diff": float(fee_diff),
            "severity": "CRITICAL" if fee_diff > Decimal("5.00") else "HIGH" if fee_diff > Decimal("0.10") else "MEDIUM",
            "regulation": REGULATION_MAP.get((tx_type, "fee"), "PSD2 Art. 62"),
        })

    # --- settled amount comparison ---
    legacy_settled = _d(legacy.get("processed_amount", 0))
    modern_settled = _d(modern.get("processed_amount", 0))
    settled_diff = abs(legacy_settled - modern_settled)
    settled_match = settled_diff <= AMOUNT_TOLERANCE

    if not settled_match:
        divergences.append({
            "field": "processed_amount",
            "legacy": float(legacy_settled),
            "modern": float(modern_settled),
            "diff": float(settled_diff),
            "severity": "HIGH" if settled_diff > Decimal("1.00") else "MEDIUM",
            "regulation": REGULATION_MAP.get((tx_type, "processed_amount"), "PSD2 Art. 62"),
        })

    # --- status match ---
    legacy_status = legacy.get("status", "")
    modern_status = modern.get("status", "")
    status_match = legacy_status == modern_status

    if not status_match:
        divergences.append({
            "field": "status",
            "legacy": legacy_status,
            "modern": modern_status,
            "diff": "status_mismatch",
            "severity": "CRITICAL",
            "regulation": STATUS_REGULATION,
        })

    # --- latency delta (informational) ---
    legacy_latency = legacy.get("processing_time_ms", 0)
    modern_latency = modern.get("processing_time_ms", 0)
    latency_improvement_pct = round(
        ((legacy_latency - modern_latency) / max(legacy_latency, 1)) * 100, 1
    )

    return {
        "transaction_id": payment["transaction_id"],
        "transaction_type": tx_type,
        "amount": payment["amount"],
        "currency": payment["currency"],
        "parity": len(divergences) == 0,
        "divergences": divergences,
        "legacy_latency_ms": legacy_latency,
        "modern_latency_ms": modern_latency,
        "latency_improvement_pct": latency_improvement_pct,
        "fee_diff": float(fee_diff),
        "settled_diff": float(settled_diff),
    }


def analyse_batch(pairs: list[dict]) -> list[dict]:
    return [compare_pair(p) for p in pairs]


def flag_anomalies(results: list[dict]) -> list[dict]:
    """Flag transactions whose fee_diff is > 2σ above the mean for their payment type."""
    import statistics
    from collections import defaultdict

    groups: dict[str, list[float]] = defaultdict(list)
    for r in results:
        groups[r["transaction_type"]].append(r["fee_diff"])

    thresholds: dict[str, tuple[float, float]] = {}
    for tx_type, diffs in groups.items():
        if len(diffs) >= 4:
            mean = statistics.mean(diffs)
            std = statistics.stdev(diffs)
            thresholds[tx_type] = (mean, std)

    for r in results:
        tx_type = r["transaction_type"]
        if tx_type in thresholds and thresholds[tx_type][1] > 0:
            mean, std = thresholds[tx_type]
            sigma = (r["fee_diff"] - mean) / std
            r["anomaly"] = sigma > 2.0 and r["fee_diff"] > 0.05
            r["anomaly_sigma"] = round(sigma, 1)
        else:
            r["anomaly"] = False
            r["anomaly_sigma"] = 0.0

    return results
