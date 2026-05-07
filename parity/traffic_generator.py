import random
import asyncio
import httpx
from services.models import PaymentRequest

LEGACY_URL = "http://localhost:8001"
MODERN_URL = "http://localhost:8002"

DOMESTIC_ACCOUNTS = [f"ACC{str(i).zfill(6)}" for i in range(1, 21)]
INTL_ACCOUNTS = [f"INTL{str(i).zfill(5)}" for i in range(1, 11)]
CURRENCIES = ["GBP", "EUR", "JPY", "CAD", "AUD"]
TX_TYPES = ["domestic", "international", "scheduled", "wire_transfer"]


def _make_payment(tx_type: str) -> PaymentRequest:
    if tx_type == "domestic":
        amount = round(random.uniform(10.0, 9999.99), 2)
        return PaymentRequest(
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            amount=amount,
            currency="USD",
            transaction_type=tx_type,
            payer_account=random.choice(DOMESTIC_ACCOUNTS),
            payee_account=random.choice(DOMESTIC_ACCOUNTS),
        )
    elif tx_type == "international":
        amount = round(random.uniform(100.0, 49999.99), 2)
        return PaymentRequest(
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            amount=amount,
            currency=random.choice(CURRENCIES),
            transaction_type=tx_type,
            payer_account=random.choice(DOMESTIC_ACCOUNTS),
            payee_account=random.choice(INTL_ACCOUNTS),
        )
    elif tx_type == "wire_transfer":
        amount = round(random.uniform(5000.0, 500000.0), 2)
        return PaymentRequest(
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            amount=amount,
            currency="USD",
            transaction_type=tx_type,
            payer_account=random.choice(DOMESTIC_ACCOUNTS),
            payee_account=random.choice(INTL_ACCOUNTS),
        )
    else:  # scheduled
        amount = round(random.uniform(1.0, 499.99), 2)
        return PaymentRequest(
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            amount=amount,
            currency="USD",
            transaction_type=tx_type,
            payer_account=random.choice(DOMESTIC_ACCOUNTS),
            payee_account=random.choice(DOMESTIC_ACCOUNTS),
        )


async def send_pair(client: httpx.AsyncClient, payment: PaymentRequest) -> dict:
    payload = payment.model_dump()
    legacy_resp, modern_resp = await asyncio.gather(
        client.post(f"{LEGACY_URL}/process_payment", json=payload),
        client.post(f"{MODERN_URL}/process_payment", json=payload),
    )
    return {
        "payment": payload,
        "legacy": legacy_resp.json(),
        "modern": modern_resp.json(),
    }


def _make_outlier_wire() -> PaymentRequest:
    """One extreme $900K wire — designed to land >2σ above the group mean fee_diff."""
    return PaymentRequest(
        transaction_id=f"TXN-{random.randint(100000, 999999)}",
        amount=900000.00,
        currency="USD",
        transaction_type="wire_transfer",
        payer_account=random.choice(DOMESTIC_ACCOUNTS),
        payee_account=random.choice(INTL_ACCOUNTS),
    )


def _make_outlier_intl() -> PaymentRequest:
    """One extreme $98K international transfer — guarantees an FX-margin anomaly."""
    return PaymentRequest(
        transaction_id=f"TXN-{random.randint(100000, 999999)}",
        amount=98000.00,
        currency=random.choice(CURRENCIES),
        transaction_type="international",
        payer_account=random.choice(DOMESTIC_ACCOUNTS),
        payee_account=random.choice(INTL_ACCOUNTS),
    )


async def run_batch(n: int = 50, weights: tuple = (0.45, 0.28, 0.15, 0.12)) -> list[dict]:
    """
    Run a batch of paired legacy/modern transactions. Demo-friendly: injects
    one extreme wire and one extreme international transaction so the >2σ
    anomaly badges always fire — without locking the random seed (run history
    still varies between runs).
    """
    forced_payments = [_make_outlier_wire(), _make_outlier_intl()]
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for p in forced_payments[:min(2, n)]:
            tasks.append(send_pair(client, p))
        for _ in range(max(0, n - 2)):
            tx_type = random.choices(TX_TYPES, weights=weights, k=1)[0]
            payment = _make_payment(tx_type)
            tasks.append(send_pair(client, payment))
        results = await asyncio.gather(*tasks)
    return list(results)
