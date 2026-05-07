"""
Legacy Bank Service — simulates a COBOL-style payment processor.

Quirks intentionally preserved:
1. ROUND_HALF_DOWN on fee calculation (COBOL default in many systems)
2. Fixed 2.0% FX conversion margin on international payments (decade-old contract)
3. Audit log emitted as fixed-width text (mainframe report style)
4. Higher latency (50–120ms) — simulates older hardware
5. Edge case: amounts ending in .X5 sometimes round inconsistently
"""

import time
import random
from decimal import Decimal, ROUND_HALF_DOWN
from datetime import datetime, timezone

from fastapi import FastAPI
import uvicorn

from services.models import PaymentRequest, PaymentResponse


app = FastAPI(title="Legacy Bank — COBOL Payment Processor", version="1.0.0")


def legacy_fee(amount: float, txn_type: str) -> Decimal:
    """COBOL-style fee with ROUND_HALF_DOWN."""
    amt = Decimal(str(amount))
    if txn_type == "domestic":
        fee = amt * Decimal("0.025") + Decimal("0.30")
    elif txn_type == "international":
        fee = amt * Decimal("0.025") + Decimal("0.30") + amt * Decimal("0.020")
    elif txn_type == "instant":
        fee = amt * Decimal("0.005") + Decimal("0.50")
    elif txn_type == "wire_transfer":
        # Legacy SWIFT pricing: 0.15% + $15 flat (decade-old contract)
        fee = amt * Decimal("0.0015") + Decimal("15.00")
    else:
        fee = amt * Decimal("0.025") + Decimal("0.30")
    return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)


def legacy_audit_log(req: PaymentRequest, fee: Decimal, total: Decimal) -> str:
    """Fixed-width mainframe-style audit record."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return (
        f"TXN={req.transaction_id:<20}"
        f"AMT={float(req.amount):>012.2f}"
        f"FEE={float(fee):>09.2f}"
        f"TOT={float(total):>012.2f}"
        f"CUR={req.currency:<3}"
        f"PAY={req.payer_account:<16}"
        f"BEN={req.payee_account:<16}"
        f"TYP={req.transaction_type:<14}"
        f"TS={ts}"
        f"SYS=COBOL/Z"
    )


@app.post("/process_payment", response_model=PaymentResponse)
def process_payment(req: PaymentRequest) -> PaymentResponse:
    start = time.time()

    # Simulate legacy hardware latency
    time.sleep(random.uniform(0.05, 0.12))

    fee = legacy_fee(req.amount, req.transaction_type)
    total = (Decimal(str(req.amount)) + fee).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_DOWN
    )

    audit = legacy_audit_log(req, fee, total)
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
        system="legacy",
    )


@app.get("/health")
def health():
    return {"status": "ok", "system": "legacy"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
