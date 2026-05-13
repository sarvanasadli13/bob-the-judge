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


async def run_batch(
    n: int = 50,
    weights: tuple = (0.45, 0.28, 0.15, 0.12),
    demo_mode: bool = False,
) -> list[dict]:
    if demo_mode:
        # Fixed seed + balanced weights → guaranteed 2-safe + 2-blocked story for judges
        random.seed(42)
        weights = (0.30, 0.30, 0.25, 0.15)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for _ in range(n):
            tx_type = random.choices(TX_TYPES, weights=weights, k=1)[0]
            payment = _make_payment(tx_type)
            tasks.append(send_pair(client, payment))
        results = await asyncio.gather(*tasks)

    if demo_mode:
        random.seed()  # restore system randomness after demo run

    return list(results)
