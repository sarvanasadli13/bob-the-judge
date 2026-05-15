# Bob Sessions — Submission Bundle

This folder contains four IBM Bob sessions captured during the development of Bob the Judge, demonstrating Bob's involvement across Plan, Edit, Ask, and Orchestrator modes.

**Captured:** 2026-05-08 (eight days before submission deadline)
**Bob version:** 1.109.5 + bob 1.0.2
**Workspace:** Bob the Judge (this repo)
**MCP integration:** Bob the Judge MCP server registered with this Bob installation under name `bob-the-judge`.

| File | Bob Mode | Outcome |
|---|---|---|
| [`A_plan.md`](A_plan.md) | Plan / Agent | 939-line v2 iteration plan with FFIEC, Basel III, PSD2, OCC, EBA citations; 4 phases, 12-sprint sequencing, 8-risk register, full SQL schema, blockchain-lite audit trail, success metrics |
| [`B_code.md`](B_code.md) | Edit | Live edits to `parity/scoring.py`: added `confidence_band` property, `score_by_tenant()` function, comprehensive docstrings; backward-compatible; tests pass |
| [`C_ask.md`](C_ask.md) | Ask | Regulator-facing memo explaining why per-function verdicts are more defensible than system-level go/no-go, citing FFIEC IT Handbook, Basel III Pillar 2, PSD2 Art. 45, SWIFT gpi SLA, NIST AI RMF |
| [`D_orchestrator.md`](D_orchestrator.md) | Orchestrator | 4-stage cutover pipeline (ANALYSER → RISK-SCOUT → FIX-GEN → REPORTER), with Stage 4 delegated to an Ask-mode sub-task — demonstrates real multi-agent meta-coordination. Cited actual codebase line `modern_bank.py:35` |

This satisfies the Lablab.ai submission requirement:
> *"Include the exported IBM Bob report of all relevant tasks/sessions used for the project."*

See [`../MAY15_BOB_CAPTURE_PLAN.md`](../MAY15_BOB_CAPTURE_PLAN.md) for the original capture plan (executed early on 2026-05-08).
See [`PROMPTS_TO_PASTE.md`](PROMPTS_TO_PASTE.md) for the four prompts used.
