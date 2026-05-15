"""
Bob client — talks to IBM Bob API when credentials are available.
Falls back to intelligent mock that mirrors Bob's real response structure
so the demo works offline and before May 15 credentials drop.
"""

import os
import json
import time
import logging
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BOB] %(message)s")
logger = logging.getLogger("bob.client")

BOB_API_KEY = os.getenv("BOB_API_KEY", "")
BOB_API_URL = os.getenv("BOB_API_URL", "https://api.ibmbob.ai/v1")

BobMode = Literal["plan", "code", "ask", "orchestrator"]


def _call_real_bob(mode: BobMode, prompt: str, context: dict) -> dict:
    """Live Bob API call — active from May 15 when credentials drop."""
    import httpx

    payload = {
        "mode": mode,
        "prompt": prompt,
        "context": context,
        "model": "bob-enterprise",
    }
    logger.info("POST %s/chat  mode=%s  key=%s...", BOB_API_URL, mode, BOB_API_KEY[:8])

    try:
        resp = httpx.post(
            f"{BOB_API_URL}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {BOB_API_KEY}"},
            timeout=30.0,
        )
        logger.info("Response %s: %s", resp.status_code, resp.text[:200])
        resp.raise_for_status()
        data = resp.json()
        # Normalise response — handle different API shapes gracefully
        if isinstance(data, dict) and "content" in data:
            return {**data, "source": "live"}
        # If the real API returns a different shape, wrap it
        return {
            "mode": mode,
            "content": data.get("message") or data.get("response") or data.get("text") or str(data),
            "model": data.get("model", "bob-enterprise"),
            "tokens_used": data.get("usage", {}).get("total_tokens", 0),
            "session_id": data.get("session_id", f"BOB-LIVE-{int(time.time())}"),
            "source": "live",
        }
    except Exception as exc:
        logger.error("Bob API call failed: %s — falling back to mock", exc)
        result = _mock_bob(mode, prompt, context)
        result["content"] = f"> ⚠️ Bob API error: `{exc}`\n> Showing intelligent mock response below.\n\n" + result["content"]
        result["source"] = "mock-fallback"
        return result


def _mock_bob(mode: BobMode, prompt: str, context: dict) -> dict:
    """
    Intelligent mock that mirrors Bob's real multi-modal response structure.
    Produces context-aware responses using the actual scores data passed in.
    """
    time.sleep(0.4)  # realistic latency

    scores = context.get("scores", [])
    safe = [s["function"] for s in scores if s["verdict"] == "SAFE_TO_CUT"]
    blocked = [s["function"] for s in scores if s["verdict"] == "DO_NOT_CUT"]
    overall_parity = context.get("overall_parity", 0)

    if mode == "plan":
        content = f"""## Bob's Migration Cutover Plan

**Assessment:** Based on {context.get('total_txns', 0):,} transactions analysed at {overall_parity:.1f}% overall parity.

### Phase 1 — Immediate Cutover (This Week)
{chr(10).join(f'- ✅ {f}' for f in safe) if safe else '- No functions cleared yet'}

### Phase 2 — Blocked (Requires Investigation)
{chr(10).join(f'- ❌ {f} — reconcile divergences before cutting over' for f in blocked) if blocked else '- None'}

### Phase 3 — Parallel Run Extension
- Extend dual-run for blocked functions by minimum 7 days
- Re-run Bob the Judge after each fix deployment
- Cutover approved only when readiness score ≥ 95

### Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Fee rounding mismatch in production | HIGH | HIGH | Reconcile FX margin logic |
| Audit log format divergence | LOW | MEDIUM | Legacy format preserved in modern system |
| Latency SLA breach | LOW | LOW | Modern system 4× faster — no risk |

**Bob recommends:** Cut approved functions now. Do not delay on cleared paths."""

    elif mode == "code":
        content = f"""## Bob's Code Fix — International FX Margin Reconciliation

The divergence in `International Wire Transfer` stems from a fee calculation mismatch.

**Root cause identified:**
```python
# Legacy (services/legacy_bank.py:32)
fee = amt * Decimal("0.025") + Decimal("0.30") + amt * Decimal("0.020")
# Fixed 2.0% FX margin — hardcoded from 2009 contract

# Modern (services/modern_bank.py) uses real-time FX spread
# This produces different settled amounts for international transfers
```

**Bob's recommended fix:**
```python
# services/modern_bank.py — add legacy-compatible FX mode
FX_LEGACY_MARGIN = Decimal("0.020")  # match legacy during parallel run

def modern_fee(amount: float, txn_type: str, legacy_compat: bool = True) -> Decimal:
    amt = Decimal(str(amount))
    base_fee = amt * Decimal("0.015") + Decimal("0.30")
    if txn_type == "international":
        # During parallel run: use legacy margin for parity
        # After cutover: switch to real-time FX (set legacy_compat=False)
        fx_margin = FX_LEGACY_MARGIN if legacy_compat else get_realtime_fx_spread()
        base_fee += amt * fx_margin
    return base_fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

**Deploy this fix → re-run Bob the Judge → International Wire should clear to SAFE_TO_CUT.**"""

    elif mode == "ask":
        content = f"""## Bob's Analysis

**Q: Is it safe to cut over now?**

**A:** Partially. Here's the breakdown:

| Function | Parity | Verdict | Action |
|----------|--------|---------|--------|
{chr(10).join(f"| {s['function']} | {s['parity_rate_pct']:.1f}% | {s['verdict'].replace('_', ' ')} | {'Cut now' if s['verdict'] == 'SAFE_TO_CUT' else 'Hold'} |" for s in scores)}

**Why is International Wire blocked?**
The legacy system uses a fixed 2.0% FX margin (contract from 2009). The modern system uses real-time spreads. This creates a fee difference on every international transaction. This is not a bug — it's a policy decision that must be resolved before cutover.

**What happens if you cut over anyway?**
Fee overcharges of ${context.get('avg_intl_diff', 648):.0f} per transaction on average. Regulatory exposure under PSD2 Article 45 (transparency of fees). Do not cut over international without reconciliation.

**Confidence in domestic cutover:** 99.1%
**Estimated time to fix international:** 2-3 hours of development."""

    else:  # orchestrator
        content = f"""## Bob Orchestrator — Automated Cutover Workflow

**Orchestrating 4-agent cutover pipeline:**

```
Agent 1 [ANALYSER]     → Scanned {context.get('total_txns', 0):,} transactions ✅
Agent 2 [RISK-SCOUT]   → Identified {len(blocked)} blocked function(s) ✅
Agent 3 [FIX-GEN]      → Generated reconciliation code for FX margin ✅
Agent 4 [REPORTER]     → Audit PDF generated and signed off ✅
```

**Orchestrated decision:**
- {', '.join(safe)} → **CUTTING OVER NOW** (automated deployment triggered)
- {', '.join(blocked) if blocked else 'None'} → **HELD** (Fix-Gen patch queued for review)

**Next automated action:** Schedule re-analysis in 24h after FX margin fix deployment.
**Audit trail:** All decisions logged with timestamp, confidence score, and Bob session ID."""

    return {
        "mode": mode,
        "content": content,
        "model": "bob-enterprise-mock",
        "tokens_used": len(content) // 4,
        "session_id": f"BOB-MOCK-{int(time.time())}",
        "source": "mock",
    }


def ask_bob(mode: BobMode, prompt: str, context: dict) -> dict:
    """Entry point — uses real Bob if API key present, mock otherwise."""
    if BOB_API_KEY:
        return _call_real_bob(mode, prompt, context)
    return _mock_bob(mode, prompt, context)
