# Bob Session Capture Launcher
# Opens IBM Bob with each of the 4 capture prompts pre-loaded.
# After each session completes, use Bob's Export Chat button to save to bob-sessions/.

$ErrorActionPreference = "Stop"
$bobide = "C:\Users\Sarvan\AppData\Local\Programs\IBM Bob\bin\bobide.cmd"
$ws = $PSScriptRoot

if (-not (Test-Path $bobide)) {
    Write-Error "IBM Bob not found at $bobide. Install it from the desktop installer first."
    exit 1
}

function Wait-User {
    param([string]$next)
    Write-Host ""
    Write-Host "  Export the previous chat to bob-sessions/ now (Bob menu -> Export Chat)."
    Write-Host "  Press ENTER when ready for: $next" -ForegroundColor Cyan
    Read-Host
}

Write-Host ""
Write-Host "===  BOB SESSION CAPTURE  ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "This will open IBM Bob 4 times sequentially with our capture prompts."
Write-Host "After each Bob response completes, EXPORT the chat to bob-sessions\\ before continuing."
Write-Host ""
Write-Host "Workspace: $ws"
Write-Host ""
Read-Host "Press ENTER to start with Session A (Plan)"

# ── Session A — agent mode (Plan) ────────────────────────────────────────────
$promptA = @'
You are advising on the next iteration of "Bob the Judge" — a per-function cutover advisor for COBOL → modern banking migrations. The current build:

- FastAPI legacy + modern bank simulators
- Parity engine with Wilson 95% CI scoring
- >2σ anomaly flagging on fee_diff distributions
- Bob client with 4 modes
- Streamlit dashboard with live patch-flip demo
- MCP server exposing 4 tools
- Audit PDF export

Plan the next iteration. What should we add to make per-function readiness scoring more rigorous and regulator-defensible? Consider: per-tenant calibration, confidence-band visualisation, drift detection across run history, FFIEC/Basel III/PSD2 alignment.

Output a phased plan with risk register and recommended sequencing.
'@

Write-Host ""
Write-Host "→ Session A: Plan (agent mode)" -ForegroundColor Green
& $bobide chat -m agent --maximize -a "parity\scoring.py" -a "parity\parity_engine.py" $promptA
Wait-User "Session B (Code, edit mode)"

# ── Session B — edit mode (Code) ──────────────────────────────────────────────
$promptB = @'
Improve parity/scoring.py with these additions, keeping the existing public API unchanged:

1. Extend the Wilson CI calculation to also return a confidence_band dict with {low, high, width} so the dashboard can visualise tightness directly.
2. Add a new function score_by_tenant(results: list[dict], tenant_id: str) -> list[dict] that filters results by tenant_id field before scoring.
3. Add a docstring example showing how to use both new outputs.

Generate the modified file as a complete diff or full replacement.
'@

Write-Host ""
Write-Host "→ Session B: Code (edit mode)" -ForegroundColor Green
& $bobide chat -m edit --maximize -a "parity\scoring.py" $promptB
Wait-User "Session C (Ask, ask mode)"

# ── Session C — ask mode (Ask) ────────────────────────────────────────────────
$promptC = @'
Explain to a banking regulator why a per-function cutover verdict (function-level readiness scoring) is more defensible than a system-level go/no-go decision during a COBOL-to-modern migration.

Cite specific frameworks where possible:
- FFIEC IT Handbook (Operations, Information Security, Audit)
- NIST AI Risk Management Framework
- Basel III operational risk
- PSD2 Article 45 (transparency of fees)
- SWIFT gpi SLA fee-consistency expectations

Frame the answer as if delivering it to a compliance officer at a mid-sized US bank in dual-run before cutover. Keep it under 500 words.
'@

Write-Host ""
Write-Host "→ Session C: Ask (ask mode)" -ForegroundColor Green
& $bobide chat -m ask --maximize $promptC
Wait-User "Session D (Orchestrator, agent mode)"

# ── Session D — agent mode (Orchestrator) ─────────────────────────────────────
$promptD = @'
Run our 4-stage cutover pipeline on these 5 sample fee_diff results:

[
  {"transaction_id": "TXN-913402", "transaction_type": "wire_transfer", "amount": 900000.00, "fee_diff": 635.00, "anomaly": true, "anomaly_sigma": 2.1},
  {"transaction_id": "TXN-447821", "transaction_type": "international", "amount": 98000.00, "fee_diff": 1960.00, "anomaly": true, "anomaly_sigma": 3.5},
  {"transaction_id": "TXN-238104", "transaction_type": "domestic", "amount": 4523.50, "fee_diff": 0.00, "anomaly": false, "anomaly_sigma": 0.0},
  {"transaction_id": "TXN-665190", "transaction_type": "scheduled", "amount": 199.99, "fee_diff": 0.00, "anomaly": false, "anomaly_sigma": 0.0},
  {"transaction_id": "TXN-119854", "transaction_type": "wire_transfer", "amount": 145000.00, "fee_diff": 102.50, "anomaly": false, "anomaly_sigma": 0.6}
]

Stages:
1. ANALYSER — categorise transactions, compute group statistics
2. RISK-SCOUT — identify functions to block, with $ exposure estimate
3. FIX-GEN — propose code-level reconciliation for the highest-severity divergence
4. REPORTER — produce a 3-line executive summary suitable for an audit PDF

Return per-stage output, then a final consolidated cutover recommendation.
'@

Write-Host ""
Write-Host "→ Session D: Orchestrator (agent mode)" -ForegroundColor Green
& $bobide chat -m agent --maximize $promptD

Write-Host ""
Write-Host "===  ALL 4 SESSIONS LAUNCHED  ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Final step: export Session D, then verify these 4 files exist:" -ForegroundColor Cyan
Write-Host "  bob-sessions\A_plan.pdf"
Write-Host "  bob-sessions\B_code.pdf"
Write-Host "  bob-sessions\C_ask.pdf"
Write-Host "  bob-sessions\D_orchestrator.pdf"
Write-Host ""
Write-Host "Then commit them to the public repo. Submission requirement satisfied." -ForegroundColor Green
