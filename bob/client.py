"""
Bob client — IBM watsonx.ai Granite primary, intelligent mock fallback.

Priority order:
  1. WATSONX_API_KEY set → real IBM Granite inference via watsonx.ai
  2. BOB_API_KEY set     → legacy Bob REST API (returns 405, falls back to mock)
  3. Neither set         → mock directly
"""

import os
import time
import logging
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BOB] %(message)s")
logger = logging.getLogger("bob.client")

BOB_API_KEY = os.getenv("BOB_API_KEY", "")
BOB_API_URL = os.getenv("BOB_API_URL", "https://api.ibmbob.ai/v1")

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
WATSONX_MODEL = os.getenv("WATSONX_MODEL", "ibm/granite-4-h-small")

BobMode = Literal["plan", "code", "ask", "orchestrator"]


def _watsonx_prompt(mode: BobMode, prompt: str, context: dict) -> str:
    """Build a mode-aware prompt for Granite."""
    scores = context.get("scores", [])
    safe = [s["function"] for s in scores if s.get("verdict") == "SAFE_TO_CUT"]
    blocked = [s["function"] for s in scores if s.get("verdict") == "DO_NOT_CUT"]
    overall_parity = context.get("overall_parity", 0)
    total_txns = context.get("total_txns", 0)

    persona = {
        "plan": "You are a senior banking migration architect producing a phased cutover plan.",
        "code": "You are a senior banking engineer producing a code fix for FX margin reconciliation.",
        "ask": "You are a banking compliance officer explaining a cutover decision to a regulator.",
        "orchestrator": "You are an orchestration agent coordinating a 4-stage cutover pipeline.",
    }[mode]

    return f"""{persona}

CONTEXT
- Transactions analysed: {total_txns:,}
- Overall parity: {overall_parity:.1f}%
- Safe to cut: {', '.join(safe) if safe else 'none'}
- Blocked: {', '.join(blocked) if blocked else 'none'}

USER QUESTION
{prompt}

Respond with structured markdown. Be concrete, cite regulatory frameworks (FFIEC, Basel III, PSD2) where relevant, and keep under 500 words.
"""


def _call_watsonx(mode: BobMode, prompt: str, context: dict) -> dict:
    """Call IBM Granite via watsonx.ai."""
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    creds = Credentials(url=WATSONX_URL, api_key=WATSONX_API_KEY)
    model = ModelInference(
        model_id=WATSONX_MODEL,
        credentials=creds,
        project_id=WATSONX_PROJECT_ID,
        params={"max_new_tokens": 700, "temperature": 0.7},
    )
    full_prompt = _watsonx_prompt(mode, prompt, context)
    logger.info("watsonx.ai %s  mode=%s  project=%s...", WATSONX_MODEL, mode, WATSONX_PROJECT_ID[:8])
    content = model.generate_text(prompt=full_prompt)
    return {
        "mode": mode,
        "content": content.strip(),
        "model": WATSONX_MODEL,
        "tokens_used": len(content) // 4,
        "session_id": f"WATSONX-{int(time.time())}",
        "source": "watsonx-granite",
    }


def _call_real_bob(mode: BobMode, prompt: str, context: dict) -> dict:
    """Legacy Bob REST API path. Bob has no REST API so this always falls back."""
    import httpx
    payload = {"mode": mode, "prompt": prompt, "context": context, "model": "bob-enterprise"}
    logger.info("POST %s/chat  mode=%s  key=%s...", BOB_API_URL, mode, BOB_API_KEY[:8])
    try:
        resp = httpx.post(
            f"{BOB_API_URL}/chat",
            json=payload,
            headers={"Authorization": f"Bearer {BOB_API_KEY}"},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        return {**data, "source": "live"}
    except Exception as exc:
        logger.error("Bob REST API failed: %s -- falling back to mock", exc)
        result = _mock_bob(mode, prompt, context)
        result["source"] = "mock-fallback"
        return result


def _mock_bob(mode: BobMode, prompt: str, context: dict) -> dict:
    """Intelligent mock — used when no watsonx/Bob credentials present."""
    time.sleep(0.4)
    scores = context.get("scores", [])
    safe = [s["function"] for s in scores if s.get("verdict") == "SAFE_TO_CUT"]
    blocked = [s["function"] for s in scores if s.get("verdict") == "DO_NOT_CUT"]
    overall_parity = context.get("overall_parity", 0)

    if mode == "plan":
        content = f"""## Bob's Migration Cutover Plan

**Assessment:** Based on {context.get('total_txns', 0):,} transactions analysed at {overall_parity:.1f}% overall parity.

### Phase 1 — Immediate Cutover (This Week)
{chr(10).join(f'- [SAFE] {f}' for f in safe) if safe else '- No functions cleared yet'}

### Phase 2 — Blocked (Requires Investigation)
{chr(10).join(f'- [HOLD] {f} — reconcile divergences before cutting over' for f in blocked) if blocked else '- None'}

### Phase 3 — Parallel Run Extension
- Extend dual-run for blocked functions by minimum 7 days
- Re-run Bob the Judge after each fix deployment
- Cutover approved only when readiness score >= 95

**Bob recommends:** Cut approved functions now. Do not delay on cleared paths."""

    elif mode == "code":
        content = """## Bob's Code Fix — International FX Margin Reconciliation

```python
# services/modern_bank.py
FX_LEGACY_MARGIN = Decimal("0.020")

def modern_fee(amount: float, txn_type: str, legacy_compat: bool = True) -> Decimal:
    amt = Decimal(str(amount))
    base_fee = amt * Decimal("0.015") + Decimal("0.30")
    if txn_type == "international":
        fx_margin = FX_LEGACY_MARGIN if legacy_compat else get_realtime_fx_spread()
        base_fee += amt * fx_margin
    return base_fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

**Deploy this fix → re-run Bob the Judge → International Wire should clear to SAFE_TO_CUT.**"""

    elif mode == "ask":
        content = f"""## Bob's Analysis

**Q: Is it safe to cut over now?**

**A:** Partially. Domestic flows at {overall_parity:.1f}% parity are clear. International Wire is blocked due to FX margin divergence (legacy 2.0% fixed margin, modern real-time spread).

**Action:** Cut over {', '.join(safe) if safe else 'cleared functions'} now. Hold {', '.join(blocked) if blocked else 'no functions'} until FX reconciliation is deployed.

**Regulatory anchor:** PSD2 Article 45 (transparency of fees), FFIEC IT Handbook section on parallel-run validation."""

    else:  # orchestrator
        content = f"""## Bob Orchestrator — Automated Cutover Workflow

```
Agent 1 [ANALYSER]     -> Scanned {context.get('total_txns', 0):,} transactions
Agent 2 [RISK-SCOUT]   -> Identified {len(blocked)} blocked function(s)
Agent 3 [FIX-GEN]      -> Generated reconciliation code for FX margin
Agent 4 [REPORTER]     -> Audit PDF generated and signed off
```

**Orchestrated decision:**
- {', '.join(safe) if safe else 'None'} -> **CUTTING OVER NOW**
- {', '.join(blocked) if blocked else 'None'} -> **HELD** for review"""

    return {
        "mode": mode,
        "content": content,
        "model": "bob-enterprise-mock",
        "tokens_used": len(content) // 4,
        "session_id": f"BOB-MOCK-{int(time.time())}",
        "source": "mock",
    }


def ask_bob(mode: BobMode, prompt: str, context: dict) -> dict:
    """Entry point — watsonx Granite primary, mock fallback."""
    if WATSONX_API_KEY and WATSONX_PROJECT_ID:
        try:
            return _call_watsonx(mode, prompt, context)
        except Exception as exc:
            logger.error("watsonx.ai failed: %s -- falling back to mock", exc)
            result = _mock_bob(mode, prompt, context)
            result["source"] = "watsonx-fallback"
            return result
    if BOB_API_KEY:
        return _call_real_bob(mode, prompt, context)
    return _mock_bob(mode, prompt, context)
