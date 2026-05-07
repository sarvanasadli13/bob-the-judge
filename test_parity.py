import asyncio
from parity.traffic_generator import run_batch
from parity.parity_engine import analyse_batch
from parity.scoring import score_results


async def main():
    print("Running 30 transaction pairs...")
    pairs = await run_batch(n=30)
    print(f"Got {len(pairs)} pairs\n")

    results = analyse_batch(pairs)
    scores = score_results(results)

    print(f"{'Function':<35} {'Parity%':>8} {'Score':>7} {'Verdict':<22}")
    print("-" * 75)
    for s in scores:
        print(
            f"{s['function']:<35} {s['parity_rate_pct']:>7.1f}% "
            f"{s['readiness_score']:>7.1f}  {s['verdict']:<22}"
        )

    print("\nSample divergences:")
    for r in results[:5]:
        if not r["parity"]:
            print(f"  {r['transaction_id']} [{r['transaction_type']}]: {r['divergences']}")


asyncio.run(main())
