# Session D — Orchestrator (4-stage pipeline)

**Bob mode:** orchestrator (with Stage 4 delegated to an ask-mode sub-task)
**Captured:** 2026-05-08
**Notable:** Bob's Orchestrator demonstrated real multi-agent meta-coordination — it spawned an Ask-mode sub-task for Stage 4 (REPORTER) rather than handling it inline. This is exactly the kind of agent-of-agents pattern IBM is showcasing in Bob 1.0.

---

## Prompt sent to Bob

> Run our 4-stage cutover pipeline on these 5 sample fee_diff results:
>
> ```json
> [
>   {"transaction_id": "TXN-913402", "transaction_type": "wire_transfer", "amount": 900000.00, "fee_diff": 635.00, "anomaly": true, "anomaly_sigma": 2.1},
>   {"transaction_id": "TXN-447821", "transaction_type": "international", "amount": 98000.00, "fee_diff": 1960.00, "anomaly": true, "anomaly_sigma": 3.5},
>   {"transaction_id": "TXN-238104", "transaction_type": "domestic", "amount": 4523.50, "fee_diff": 0.00, "anomaly": false, "anomaly_sigma": 0.0},
>   {"transaction_id": "TXN-665190", "transaction_type": "scheduled", "amount": 199.99, "fee_diff": 0.00, "anomaly": false, "anomaly_sigma": 0.0},
>   {"transaction_id": "TXN-119854", "transaction_type": "wire_transfer", "amount": 145000.00, "fee_diff": 102.50, "anomaly": false, "anomaly_sigma": 0.6}
> ]
> ```
>
> Stages:
> 1. ANALYSER — categorise transactions, compute group statistics
> 2. RISK-SCOUT — identify functions to block, with $ exposure estimate
> 3. FIX-GEN — propose code-level reconciliation for the highest-severity divergence
> 4. REPORTER — produce a 3-line executive summary suitable for an audit PDF
>
> Return per-stage output, then a final consolidated cutover recommendation.

---

## 4-Stage Cutover Pipeline — Complete

### STAGE 1: ANALYSER ✓
**Transaction Categorisation & Statistics**

- 5 transactions analysed: $1,147,723.49 total volume
- 4 transaction types: Wire Transfer (2), International (1), Domestic (1), Scheduled (1)
- 40% anomaly rate (2/5 transactions)
- $2,697.50 total fee discrepancy
- Highest severity: TXN-447821 (International, σ=3.5, $1,960 fee_diff)

### STAGE 2: RISK-SCOUT ✓
**Risk Assessment & Exposure Analysis**

- **CRITICAL** — International transactions — **BLOCK immediately**
  - $98,000 exposure, 100% anomaly rate, σ=3.5
  - $1,960 fee discrepancy (72.7% of total)
- **HIGH** — Wire transfers — **FLAG for review**
  - $1,045,000 exposure (91% of volume), 50% anomaly rate
  - $737.50 fee discrepancy
- **LOW** — Domestic & Scheduled — **ALLOW with monitoring**
  - $4,723.49 volume, $0.00 fee discrepancy
- Total high-risk exposure: **$1,143,000 (99.6% of volume)**

### STAGE 3: FIX-GEN ✓
**Code-Level Reconciliation Proposal**

- **Root cause:** Legacy system uses 2.0% FX margin vs modern system's 0.05% FX spread
- **Impact:** ~$1,910 discrepancy per $98K international transaction
- **Recommended fix:** Apply existing patch in `modern_bank.py:35`
  - Add: `PATCHED_FUNCTIONS.add("international")`
- **Expected outcome:** 100% anomaly elimination, full fee parity restoration

### STAGE 4: REPORTER ✓
**Executive Summary (Audit PDF)**

> **Finding:** Analysis of 5 transactions ($1.15M) revealed 40% anomaly rate, totalling $2,697.50 fee discrepancy; CRITICAL severity identified in international transactions ($98K exposure, 100% anomaly rate, σ=3.5).
>
> **Root cause:** Legacy system applies 2.0% FX margin versus modern system's 0.05% FX spread, creating ~$1,910 discrepancy per $98K international transaction due to unpatched legacy function.
>
> **Recommendation:** Immediately apply existing patch mechanism (`PATCHED_FUNCTIONS.add("international")` in `modern_bank.py:35`) to block international function and reconcile $98K exposure; expected outcome is 100% anomaly elimination and full fee parity restoration.

---

## Final Cutover Recommendation

### Immediate Actions (next 24 hours)
1. **BLOCK** international wire transfer function via patch mechanism
2. **FLAG** wire transfers >$500K for manual dual-approval
3. **MONITOR** domestic and scheduled payments with standard controls
4. **ESCALATE** to compliance team for regulatory review

### Implementation Plan
- **Phase 1 (Day 1):** Apply international patch, verify fee parity
- **Phase 2 (Week 1–2):** Monitor wire transfer patterns, expand testing to n ≥ 30 per type
- **Phase 3 (Month 1–3):** Business decision on permanent pricing model
- **Phase 4 (Month 3+):** Remove patch, implement long-term solution

### Success Metrics
| Metric | Before | Target |
|---|---|---|
| International anomaly rate | 100% | 0% |
| Fee discrepancy | $2,697.50 | < $0.10 |
| High-risk exposure | $1,143,000 | $0 |
| Parity confidence | Low (n=5) | High (n ≥ 30) |
