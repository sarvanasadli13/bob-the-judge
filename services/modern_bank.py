"""
Modern Bank Service — modernized payment processor (Python/FastAPI rewrite).

Intentional divergences from legacy:
1. ROUND_HALF_UP on fee calculation (modern banking standard, IFRS-friendly)
2. Real-time FX with 5 bps spread on international (replaces legacy fixed 2.0%)
3. Audit log emitted as JSON (modern observability format)
4. Lower latency (5–20ms) — modern infrastructure
5. Edge case rounding is now consistent

These divergences are what Bob the Judge has to evaluate.
"""

import json
import time
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
from datetime import datetime, timezone

from fastapi import FastAPI
import uvicorn

from services.models import PaymentRequest, PaymentResponse


app = FastAPI(title="Modern Bank — Python Payment Processor", version="2.0.0")


# Simulated real-time FX spread (5 bps = 0.05%)
FX_SPREAD = Decimal("0.0005")

# Bob's live patch state — when a function is patched, modern uses legacy formula
# to maintain parity during the dual-run window (cleared on /admin/reset_patches).
PATCHED_FUNCTIONS: set = set()


def modern_fee(amount: float, txn_type: str) -> Decimal:
    """Modern fee with ROUND_HALF_UP. Bob's patch can switch a function to legacy formula."""
    amt = Decimal(str(amount))

    # ── Bob's parallel-run compatibility patch ───────────────────────────────
    if txn_type == "international" and "international" in PATCHED_FUNCTIONS:
        # Patch: temporarily match legacy fixed 2.0% FX margin
        fee = amt * Decimal("0.025") + Decimal("0.30") + amt * Decimal("0.020")
        return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)
    if txn_type == "wire_transfer" and "wire_transfer" in PATCHED_FUNCTIONS:
        # Patch: align with legacy SWIFT pricing for parity
        fee = amt * Decimal("0.0015") + Decimal("15.00")
        return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)

    # ── Default modern fee logic ─────────────────────────────────────────────
    if txn_type == "domestic":
        fee = amt * Decimal("0.025") + Decimal("0.30")
    elif txn_type == "international":
        # Real-time FX: small spread instead of legacy fixed 2.0%
        fx_jitter = Decimal(str(random.uniform(-0.0002, 0.0008)))
        fee = amt * Decimal("0.025") + Decimal("0.30") + amt * (FX_SPREAD + fx_jitter)
    elif txn_type == "instant":
        fee = amt * Decimal("0.005") + Decimal("0.50")
    elif txn_type == "wire_transfer":
        # Modern pricing: 0.08% + $10 flat (replaces legacy SWIFT contract)
        fee = amt * Decimal("0.0008") + Decimal("10.00")
    else:
        fee = amt * Decimal("0.025") + Decimal("0.30")
    return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def modern_audit_log(req: PaymentRequest, fee: Decimal, total: Decimal) -> str:
    """Structured JSON audit record."""
    payload = {
        "txn_id": req.transaction_id,
        "amount": float(req.amount),
        "fee": float(fee),
        "total": float(total),
        "currency": req.currency,
        "payer": req.payer_account,
        "payee": req.payee_account,
        "type": req.transaction_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": "python/modern",
    }
    return json.dumps(payload, separators=(",", ":"))


@app.post("/process_payment", response_model=PaymentResponse)
def process_payment(req: PaymentRequest) -> PaymentResponse:
    start = time.time()

    # Modern infrastructure latency
    time.sleep(random.uniform(0.005, 0.020))

    fee = modern_fee(req.amount, req.transaction_type)
    total = (Decimal(str(req.amount)) + fee).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    audit = modern_audit_log(req, fee, total)
    elapsed = (time.time() - start) * 1000

    return PaymentResponse(
        transaction_id=req.transaction_id,
        processed_amount=float(Decimal(str(req.amount)).quantize(Decimal("0.01"))),
        fee=float(fee),
        total_charged=float(total),
        currency=req.currency,
        status="approved",
        audit_log=audit,
        processing_time_ms=round(elapsed, 2),
        system="modern",
    )


@app.get("/health")
def health():
    return {"status": "ok", "system": "modern", "patched": list(PATCHED_FUNCTIONS)}


@app.post("/admin/apply_patch")
def apply_patch(payload: dict = None):
    """
    Apply Bob's parallel-run compatibility patch.
    With no body: patches all known divergent functions.
    With {"function": "<name>"}: patches that one function only.
    """
    if payload and payload.get("function"):
        PATCHED_FUNCTIONS.add(payload["function"])
    else:
        PATCHED_FUNCTIONS.update(["international", "wire_transfer"])
    return {"patched": sorted(PATCHED_FUNCTIONS), "status": "active"}


@app.post("/admin/reset_patches")
def reset_patches():
    """Restore original modern bank fee logic (remove Bob's patch)."""
    PATCHED_FUNCTIONS.clear()
    return {"patched": [], "status": "cleared"}


@app.get("/admin/patches")
def list_patches():
    return {"patched": sorted(PATCHED_FUNCTIONS)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
