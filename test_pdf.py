import asyncio
from parity.traffic_generator import run_batch
from parity.parity_engine import analyse_batch
from parity.scoring import score_results
from audit.pdf_report import generate_pdf

async def main():
    print("Running transactions...")
    pairs = await run_batch(n=40)
    results = analyse_batch(pairs)
    scores = score_results(results)
    print(f"Scores: {[s['verdict'] for s in scores]}")

    print("Generating PDF...")
    pdf_bytes = generate_pdf(scores, results)
    out = "audit_test.pdf"
    with open(out, "wb") as f:
        f.write(pdf_bytes)
    print(f"PDF written: {len(pdf_bytes):,} bytes -> {out}")

asyncio.run(main())
