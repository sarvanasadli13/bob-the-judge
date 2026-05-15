# Bob Sessions — Hackathon Submission Bundle

This folder contains four IBM Bob task session reports captured on **2026-05-15** (hackathon day 1) using the IBM Bob IDE on the hackathon-provisioned account, demonstrating Bob's involvement across **Plan, Code (Edit), Ask, and Orchestrator** modes.

**Bob version:** 1.109.5 + bob 1.0.2
**Workspace:** `C:\Users\Sarvan\projects\bob-the-judge`
**Account:** Hackathon-provisioned (`ibm-coding-challenge-xxx`)
**Captured per:** [IBM Bob Hackathon Guide, page 18 — "Exporting Bob task session reports for judging"]

## Sessions

| File | Bob Mode | Outcome |
|---|---|---|
| [`A_plan.md`](A_plan.md) + [`A_plan_consumption.png`](A_plan_consumption.png) | **Plan / Agent** | Full v2 iteration roadmap with FFIEC, Basel III, PSD2 citations. Then implemented **Phase 1 — Per-Tenant Calibration**: created `parity/tenant_config.py`, `config/tenants.json` (4 tier profiles), updated `parity/parity_engine.py` and `parity/scoring.py`. Real code committed to repo. |
| [`B_code.md`](B_code.md) + [`B_code_consumption.png`](B_code_consumption.png) | **Code / Edit** | Added `format_score_summary(scores: list[FunctionScore]) -> str` helper to `parity/scoring.py` for CLI/log output. 24 lines, zero external imports, backward compatible. |
| [`C_ask.md`](C_ask.md) + [`C_ask_consumption.png`](C_ask_consumption.png) | **Ask** | Regulator-facing memo explaining why per-function verdicts are more defensible than system-level go/no-go, citing FFIEC IT Handbook, Basel III Pillar 1, NIST AI RMF, PSD2 Art. 45, SWIFT gpi SLA. |
| [`D_orchestrato_sum.md`](D_orchestrato_sum.md) + 4 sub-task files (`D_orchestrator1-4.md`) + [`D_orchestrator_consumption.png`](D_orchestrator_consumption.png) | **Orchestrator** | 4-stage cutover pipeline (ANALYSER → RISK-SCOUT → FIX-GEN → REPORTER). Bob delegated each stage to specialised sub-tasks in Ask/Code modes — real multi-agent meta-coordination demonstrated. |

## What this satisfies

> *"Participants are required to export and upload Bob IDE task session report in their code repository for judging purposes."* — IBM Bob Hackathon Guide

Each markdown file is the **exported task history** from Bob IDE's History view, and each PNG is the corresponding **task session consumption summary** screenshot, as required by the guide.

## Prompts used

See [`PROMPTS_TO_PASTE.md`](PROMPTS_TO_PASTE.md) for the four prompts (slightly adapted at the moment of capture).
