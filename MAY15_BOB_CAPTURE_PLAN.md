# May 15 — Bob Session Export Capture Plan

> **Status: COMPLETE — captured early on 2026-05-08.** IBM Bob 1.109.5 was already available on the dev machine, so all four sessions were captured eight days ahead of schedule. See `bob-sessions/` for the bundle. The plan below is preserved as the historical capture procedure.

**Why this exists:** Lablab.ai submission rules require *"the exported IBM Bob report of all relevant tasks/sessions used for the project."* Without it, Project Completion score drops. This plan ensures the moment real Bob credentials drop on May 15, we capture qualifying sessions and bundle them with the submission.

---

## Pre-flight (May 14 evening)

- [ ] Verify repo is **public** on GitHub (Lablab penalises private repos)
- [ ] Confirm `BOB_API_KEY` env var slot is wired in `bob/client.py` (already done — switches `_call_real_bob` vs mock automatically)
- [ ] Confirm `BOB_API_URL` defaults to `https://api.ibmbob.ai/v1` — update if IBM publishes a different endpoint at kick-off
- [ ] Pre-write the 4 prompts below into a notes file so we can paste them in fast on the 15th
- [ ] Confirm `mcp_server.py` runs cleanly and `bob-mcp-config.json` points to the right path

## Kick-off morning, May 15

1. Receive Bob API credentials from IBM/Lablab kick-off stream
2. Set the env vars in a fresh shell:
   ```powershell
   $env:BOB_API_KEY = "<key>"
   $env:BOB_API_URL = "<url-from-stream-if-different>"
   ```
3. Run `python -c "from bob.client import ask_bob; print(ask_bob('plan', 'sanity check', {}))"` — confirm a real Bob response comes back, not the mock
4. If the call fails, fall back to mock for the demo — but keep retrying real Bob for the export bundle

## The 4 capture sessions (run inside Bob's IDE, not from our app)

These are the sessions we will export and bundle with the submission. Each one demonstrates Bob assisting in our development.

**Session A — Plan mode**
- Prompt: *"We are building Bob the Judge, a per-function cutover advisor for COBOL → modern banking migrations. Plan the next iteration: what should we add to make the per-function readiness scoring more rigorous? Consider Wilson CI, anomaly flagging, and per-tenant calibration."*
- Capture: full Bob response + any code suggestions

**Session B — Code mode**
- Prompt: *"Here is `parity/scoring.py`. Improve the Wilson CI calculation to also return a confidence band, and add a function `score_by_tenant(results, tenant_id)` that filters results before scoring. Keep the existing public API unchanged."*
- Paste the contents of `parity/scoring.py`
- Capture: Bob's diff/code output

**Session C — Ask mode**
- Prompt: *"Explain to a banking regulator why a per-function cutover verdict (function-level readiness) is more defensible than a system-level go/no-go. Cite frameworks where possible (FFIEC, NIST AI RMF)."*
- Capture: explanation paragraph

**Session D — Orchestrator mode**
- Prompt: *"Run our 4-stage pipeline on these sample fee_diff results: [paste 5 sample dicts from a real run]. Stages: Analyser → Risk-Scout → Fix-Generator → Reporter. Return per-stage output."*
- Capture: orchestrator stage-by-stage output

## Export & bundle

- [ ] Inside Bob IDE → Export each session as PDF or transcript file (whatever Bob's export feature produces — Lablab rules say "Bob report")
- [ ] Save all 4 exports into a new project folder: `bob-sessions/`
  - `bob-sessions/A_plan.pdf`
  - `bob-sessions/B_code.pdf`
  - `bob-sessions/C_ask.pdf`
  - `bob-sessions/D_orchestrator.pdf`
- [ ] Add `bob-sessions/README.md` with one-line summary of each
- [ ] Commit and push to public repo
- [ ] Reference `bob-sessions/` in the main project README

## Live demo on May 15–16

- During the rehearsal, set `BOB_API_KEY` and run the dashboard once with real Bob to confirm the patch-flip moment still works end-to-end
- If real Bob is slow or flaky, switch back to the mock client for the recorded video (mock is intentionally instant) — but keep real Bob in the GitHub commit history so judges see we wired it

## Submission checklist (May 17 before 08:00 PDT)

- [ ] Public GitHub repo URL
- [ ] `bob-sessions/` folder with all 4 exports committed
- [ ] Recorded demo video uploaded
- [ ] Pitch deck PDF uploaded
- [ ] Project description references the Bob session bundle
- [ ] `requirements.txt` pins `starlette<1.0.0` (already done)
- [ ] Final smoke test: clone repo into a fresh folder, run `pip install -r requirements.txt && python launch.py` — confirm dashboard, MCP server, and patch flip all work

## Failure modes to guard against

| Risk | Mitigation |
|---|---|
| Bob API credentials never arrive | Submit with mock + a clear note in README; capture sessions through the public Bob playground if one exists |
| Bob export feature does not produce a clean PDF | Save raw transcripts + screenshots as fallback; bundle both |
| Real Bob latency breaks the live demo | Pre-record the video with the mock client (instant), keep real Bob for the audit bundle only |
| MCP connection from real Bob IDE fails | Demo MCP feature using the standalone `mcp_server.py` console output as evidence |

---

**One-line summary:** On May 15 morning, set `BOB_API_KEY`, run 4 prompts inside Bob's IDE (Plan, Code, Ask, Orchestrator), export all 4 sessions, commit them under `bob-sessions/` in the public repo, then submit.
