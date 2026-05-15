# Bob Session Capture — Ready-to-Paste Prompts

**Two ways to run these:**

### Option A — One-shot CLI launch (fastest)
Run `.\capture-sessions.ps1` from the project root. It opens IBM Bob with each prompt pre-loaded in the right mode. After each completes, use Bob's **Export Chat** button → save to `bob_sessions/` with the filename shown.

### Option B — Manual paste
Open **IBM Bob** desktop, open this workspace folder, copy each prompt below into the chat panel. After each Bob response completes:

1. Use Bob's built-in **export / save chat** feature.
2. Save as PDF (preferred) or `.md` to this folder with the filename shown.
3. After all 4 are done, the `bob_sessions/` folder satisfies the Lablab submission requirement.

**Bob mode mapping** — IBM Bob 1.109.5 supports three CLI modes: `ask`, `edit`, `agent`. We map our 4 capture sessions to:

| Session | IBM Bob mode | Reason |
|---|---|---|
| A — Plan | `agent` | Multi-step planning |
| B — Code | `edit` | Code modifications to existing file |
| C — Ask | `ask` | Plain Q&A with regulator framing |
| D — Orchestrator | `agent` | Multi-stage pipeline reasoning |

---

## Session A — Plan mode  →  save as `A_plan.pdf`

**Mode:** Plan (or whichever IBM Bob mode generates phased roadmaps)

**Paste this prompt:**

```
You are advising on the next iteration of "Bob the Judge" — a per-function
cutover advisor for COBOL → modern banking migrations. The current build:

- FastAPI legacy + modern bank simulators (services/legacy_bank.py, services/modern_bank.py)
- Parity engine with Wilson 95% CI scoring (parity/parity_engine.py, parity/scoring.py)
- >2σ anomaly flagging on fee_diff distributions
- Bob client with 4 modes (bob/client.py)
- Streamlit dashboard (dashboard.py) with live patch-flip demo
- MCP server exposing 4 tools (mcp_server.py)
- Audit PDF export (audit/pdf_report.py)

Plan the next iteration. What should we add to make per-function readiness
scoring more rigorous and regulator-defensible? Consider:
- Per-tenant calibration (different banks have different parity tolerances)
- Confidence-band visualisation beyond Wilson CI
- Drift detection across run history
- FFIEC, Basel III, PSD2 alignment

Output a phased plan with risk register and recommended sequencing.
```

---

## Session B — Code mode  →  save as `B_code.pdf`

**Mode:** Code

**Paste this prompt:**

```
Improve parity/scoring.py with these additions, keeping the existing public API
unchanged:

1. Extend the Wilson CI calculation to also return a confidence_band dict with
   {low, high, width} so the dashboard can visualise tightness directly.
2. Add a new function `score_by_tenant(results: list[dict], tenant_id: str) -> list[dict]`
   that filters results by tenant_id field before scoring.
3. Add a docstring example showing how to use both new outputs.

Below is the current scoring.py. Generate the modified file as a complete diff
or full replacement.

[Paste contents of parity/scoring.py here when running]
```

*(Open `parity/scoring.py` in IBM Bob first, then run this prompt — Bob will see the file in context.)*

---

## Session C — Ask mode  →  save as `C_ask.pdf`

**Mode:** Ask

**Paste this prompt:**

```
Explain to a banking regulator why a per-function cutover verdict
(function-level readiness scoring) is more defensible than a system-level
go/no-go decision during a COBOL-to-modern migration.

Cite specific frameworks where possible:
- FFIEC IT Handbook (Operations, Information Security, Audit)
- NIST AI Risk Management Framework
- Basel III operational risk
- PSD2 Article 45 (transparency of fees)
- SWIFT gpi SLA fee-consistency expectations

Frame the answer as if delivering it to a compliance officer at a mid-sized
US bank in dual-run before cutover. Keep it under 500 words.
```

---

## Session D — Orchestrator mode  →  save as `D_orchestrator.pdf`

**Mode:** Orchestrator (or Agentic / Multi-step if your Bob version uses different naming)

**Paste this prompt:**

```
Run our 4-stage cutover pipeline on these 5 sample fee_diff results:

[
  {"transaction_id": "TXN-913402", "transaction_type": "wire_transfer",
   "amount": 900000.00, "fee_diff": 635.00, "anomaly": true, "anomaly_sigma": 2.1},
  {"transaction_id": "TXN-447821", "transaction_type": "international",
   "amount": 98000.00, "fee_diff": 1960.00, "anomaly": true, "anomaly_sigma": 3.5},
  {"transaction_id": "TXN-238104", "transaction_type": "domestic",
   "amount": 4523.50, "fee_diff": 0.00, "anomaly": false, "anomaly_sigma": 0.0},
  {"transaction_id": "TXN-665190", "transaction_type": "scheduled",
   "amount": 199.99, "fee_diff": 0.00, "anomaly": false, "anomaly_sigma": 0.0},
  {"transaction_id": "TXN-119854", "transaction_type": "wire_transfer",
   "amount": 145000.00, "fee_diff": 102.50, "anomaly": false, "anomaly_sigma": 0.6}
]

Stages:
1. ANALYSER  — categorise transactions, compute group statistics
2. RISK-SCOUT — identify functions to block, with $ exposure estimate
3. FIX-GEN   — propose code-level reconciliation for the highest-severity divergence
4. REPORTER  — produce a 3-line executive summary suitable for an audit PDF

Return per-stage output, then a final consolidated cutover recommendation.
```

---

## After capture

- Verify all 4 PDFs/files saved in `bob_sessions/`
- Update `bob_sessions/README.md` with the actual capture date (replace "May 15")
- Commit and push to the public GitHub repo
- Reference `bob_sessions/` in main README and submission description

**Total time estimate:** 20–30 minutes interactive with IBM Bob.
