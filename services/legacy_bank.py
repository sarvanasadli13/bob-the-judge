"""
Legacy Bank Service — COBOL-style payment processor.

Fee logic lives in services/cobol/FEE_CALC.cob (GnuCOBOL 3.x).
At startup the service attempts to compile and run the COBOL binary.
Falls back to identical Python logic if GnuCOBOL (cobc) is not installed.

Intentional legacy quirks preserved in both paths:
1. ROUND_HALF_DOWN on every fee (COBOL z/OS default)
2. Fixed 2.0% FX margin on international (2009 contract, never updated)
3. Audit log emitted as fixed-width mainframe record (COBOL/Z style)
4. Higher latency (50–120 ms) — simulates z15 batch queue
"""

import os
import platform
import shutil
import subprocess
import time
import random
import logging
from decimal import Decimal, ROUND_HALF_DOWN
from datetime import datetime, timezone

from fastapi import FastAPI
import uvicorn

from services.models import PaymentRequest, PaymentResponse

logger = logging.getLogger("legacy_bank")

# ── COBOL binary paths ──────────────────────────────────────────────
_DIR     = os.path.dirname(os.path.abspath(__file__))
_COB_SRC = os.path.join(_DIR, "cobol", "FEE_CALC.cob")
_COB_BIN = os.path.join(
    _DIR, "cobol",
    "fee_calc.exe" if platform.system() == "Windows" else "fee_calc"
)

_cobol_ready: bool | None = None   # None = not yet probed


def _init_cobol() -> bool:
    """Compile FEE_CALC.cob once at startup. Returns True if COBOL is usable."""
    global _cobol_ready
    if _cobol_ready is not None:
        return _cobol_ready

    if not shutil.which("cobc"):
        logger.info("cobc not found — using Python fee fallback (COBOL source at services/cobol/FEE_CALC.cob)")
        _cobol_ready = False
        return False

    if not os.path.exists(_COB_BIN):
        result = subprocess.run(
            ["cobc", "-x", "-o", _COB_BIN, _COB_SRC],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.warning("COBOL compile failed: %s", result.stderr)
            _cobol_ready = False
            return False

    logger.info("COBOL binary ready: %s", _COB_BIN)
    _cobol_ready = True
    return True


def _fee_via_cobol(amount: float, txn_type: str) -> Decimal:
    """Call the compiled FEE_CALC binary via stdin/stdout."""
    result = subprocess.run(
        [_COB_BIN],
        input=f"{amount}\n{txn_type}\n",
        capture_output=True,
        text=True,
        timeout=5,
    )
    raw = result.stdout.strip()
    return Decimal(raw).quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)


def _fee_python(amount: float, txn_type: str) -> Decimal:
    """Pure-Python mirror of FEE_CALC.cob — identical arithmetic."""
    amt = Decimal(str(amount))
    if txn_type == "domestic":
        fee = amt * Decimal("0.025") + Decimal("0.30")
    elif txn_type == "international":
        fee = amt * Decimal("0.025") + Decimal("0.30") + amt * Decimal("0.020")
    elif txn_type == "instant":
        fee = amt * Decimal("0.005") + Decimal("0.50")
    elif txn_type == "wire_transfer":
        fee = amt * Decimal("0.0015") + Decimal("15.00")
    else:
        fee = amt * Decimal("0.025") + Decimal("0.30")
    return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_DOWN)


def legacy_fee(amount: float, txn_type: str) -> tuple[Decimal, str]:
    """
    Compute fee. Returns (fee, engine) where engine is 'COBOL/Z' or 'COBOL/Z-PY'.
    COBOL/Z   = GnuCOBOL binary executed.
    COBOL/Z-PY = Python fallback (cobc not installed).
    """
    if _init_cobol():
        try:
            return _fee_via_cobol(amount, txn_type), "COBOL/Z"
        except Exception as exc:
            logger.warning("COBOL runtime error (%s) — falling back to Python", exc)
    return _fee_python(amount, txn_type), "COBOL/Z-PY"


def legacy_audit_log(req: PaymentRequest, fee: Decimal, total: Decimal, engine: str) -> str:
    """Fixed-width mainframe-style audit record (IBM z/OS VSAM format)."""
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
        f"SYS={engine}"
    )


# ── FastAPI app ─────────────────────────────────────────────────────
app = FastAPI(title="Legacy Bank — COBOL Payment Processor", version="1.0.0")


@app.on_event("startup")
def startup():
    _init_cobol()


@app.post("/process_payment", response_model=PaymentResponse)
def process_payment(req: PaymentRequest) -> PaymentResponse:
    start = time.time()
    time.sleep(random.uniform(0.05, 0.12))   # z15 batch queue latency

    fee, engine = legacy_fee(req.amount, req.transaction_type)
    total = (Decimal(str(req.amount)) + fee).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_DOWN
    )
    audit  = legacy_audit_log(req, fee, total, engine)
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
    cobol = _init_cobol()
    return {
        "status": "ok",
        "system": "legacy",
        "fee_engine": "COBOL/Z (GnuCOBOL)" if cobol else "COBOL/Z-PY (Python fallback)",
        "cobol_source": "services/cobol/FEE_CALC.cob",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
