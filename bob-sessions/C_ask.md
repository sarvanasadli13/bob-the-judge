# Session C — Ask (regulator framing)

**Bob mode:** ask
**Captured:** 2026-05-08
**Audience:** Compliance officer at a mid-sized US bank in dual-run before cutover

---

## Prompt sent to Bob

> Explain to a banking regulator why a per-function cutover verdict (function-level readiness scoring) is more defensible than a system-level go/no-go decision during a COBOL-to-modern migration.
>
> Cite specific frameworks where possible:
> - FFIEC IT Handbook (Operations, Information Security, Audit)
> - NIST AI Risk Management Framework
> - Basel III operational risk
> - PSD2 Article 45 (transparency of fees)
> - SWIFT gpi SLA fee-consistency expectations
>
> Frame the answer as if delivering it to a compliance officer at a mid-sized US bank in dual-run before cutover. Keep it under 500 words.

---

## Bob's response

# Per-Function Cutover Verdicts: A Regulatory Defense Framework

**To:** Compliance Officer, Mid-Sized US Bank
**Re:** Function-Level Readiness Scoring During Dual-Run Migration

## Executive Summary

A per-function cutover verdict provides granular, auditable evidence that each business capability meets regulatory standards before production release. This approach directly addresses regulatory expectations for operational resilience, risk management, and consumer protection that a binary system-level go/no-go decision cannot satisfy.

## Regulatory Alignment

### 1. FFIEC IT Handbook — Operations & Audit

The FFIEC Operations booklet mandates "appropriate testing" and "documented evidence of system readiness." Per-function scoring creates an audit trail for each capability (e.g., wire transfers, ACH processing, fee calculations), demonstrating that testing was neither superficial nor monolithic. When examiners ask "How do you know payment processing is ready?", you present function-specific test results, not a single system checkbox.

### 2. Basel III Operational Risk (Pillar 2)

Basel III requires banks to identify, measure, and mitigate operational risk. A system-level decision treats migration as a single risk event. Per-function verdicts enable risk-weighted cutover sequencing — you migrate low-risk functions (account inquiries) before high-risk ones (international wire transfers), reducing aggregate operational risk exposure and demonstrating proportionate risk management to regulators.

### 3. PSD2 Article 45 — Fee Transparency

PSD2 mandates transparent, consistent fee calculations. During migration, fee logic is particularly sensitive. A per-function verdict for the fee calculation module provides specific evidence that:

- Legacy and modern systems produce identical fees for identical transactions
- Edge cases (foreign exchange, tiered pricing) are validated independently
- Discrepancies are documented and resolved before cutover

This granularity is indefensible with a system-level decision that obscures fee-calculation readiness within broader "payments system" approval.

### 4. SWIFT gpi SLA — Fee Consistency

SWIFT gpi requires end-to-end fee transparency and consistency. Per-function scoring allows you to isolate SWIFT message generation and validate that fee fields (charges, intermediary fees) match legacy output byte-for-byte. If your system-level test passes but SWIFT fees diverge post-cutover, you face correspondent bank disputes and regulatory scrutiny. Function-level verdicts prevent this by proving SWIFT-specific readiness.

### 5. NIST AI RMF — Trustworthiness & Transparency

If your modern system incorporates ML-based fraud detection or credit decisioning, NIST AI RMF demands function-specific validation of fairness, explainability, and accuracy. A system-level decision cannot demonstrate that AI-driven components meet trustworthiness criteria independently from deterministic functions like balance calculations.

## Practical Defense During Examination

When regulators review your dual-run results:

- **System-level decision:** "We tested the entire system and it passed."
- **Per-function verdict:** "We scored 47 business functions. Wire transfers achieved 99.97% parity across 10,000 transactions. Fee calculations matched 100% with documented exceptions for three legacy rounding bugs we corrected."

The latter is defensible, auditable, and demonstrates due diligence. It also enables partial cutover — migrating proven functions while keeping risky ones in legacy — reducing operational risk and satisfying FFIEC's "appropriate controls" standard.

## Conclusion

Per-function cutover verdicts transform migration from a binary gamble into a measured, evidence-based process that aligns with regulatory expectations for operational resilience, risk management, and consumer protection. This approach is not merely best practice — it's regulatory prudence.
