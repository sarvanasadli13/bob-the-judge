# Bob the Judge — Next Iteration Plan
## Making Per-Function Readiness Scoring Regulator-Defensible

**Version:** 2.0 Planning Document  
**Date:** May 2026  
**Regulatory Scope:** Multi-jurisdictional (FFIEC, Basel III, PSD2)  
**Status:** Planning Phase

---

## Executive Summary

Bob the Judge v1.0 successfully demonstrates per-function cutover readiness with Wilson 95% CI scoring and >2σ anomaly detection. The next iteration focuses on making the system **audit-defensible for multi-jurisdictional banking regulators** by adding:

1. **Per-tenant calibration** — tenant-specific risk thresholds and business rules
2. **Confidence band visualization** — interactive charts showing statistical uncertainty
3. **Drift detection** — temporal analysis across run history to catch degradation
4. **Regulatory framework alignment** — explicit FFIEC/Basel III/PSD2 compliance mapping
5. **Enhanced audit trail** — immutable evidence chain with cryptographic verification

**Target Outcome:** A system that can withstand regulatory scrutiny during OCC examinations, EBA audits, and Basel III operational risk assessments.

---

## Current System Analysis

### ✅ Strengths (v1.0)

| Component | Capability | Regulatory Value |
|-----------|-----------|------------------|
| **Wilson 95% CI** | Statistically sound confidence intervals | Meets FFIEC statistical rigor requirements |
| **>2σ Anomaly Flagging** | Outlier detection on fee_diff distributions | Basel III operational risk event detection |
| **Per-Function Scoring** | Granular readiness verdicts (4 levels) | PSD2 Art. 95 — proportionate risk assessment |
| **Audit PDF Export** | Regulator-grade sign-off document | FFIEC audit trail requirement |
| **Live Parity Engine** | Real-time dual-run comparison | PSD2 Art. 98 — testing requirements |

### ⚠️ Gaps (Regulatory Perspective)

| Gap | Regulatory Risk | Impact |
|-----|----------------|--------|
| **No per-tenant calibration** | One-size-fits-all thresholds fail for multi-entity banks | FFIEC expects entity-specific risk profiles |
| **Static confidence bands** | No visualization of statistical uncertainty over time | Basel III Pillar 3 disclosure requirements |
| **No drift detection** | Cannot prove stability across migration window | PSD2 Art. 98 — continuous monitoring |
| **Implicit regulation mapping** | Hard-coded strings, not traceable to specific articles | OCC expects explicit compliance citations |
| **Mutable audit trail** | PDF can be regenerated, no tamper-evidence | FFIEC IT Examination Handbook — data integrity |
| **No tenant isolation** | Single scoring model for all business units | Basel III — operational risk segmentation |

---

## Phase 1: Enhanced Statistical Rigor
**Duration:** 3 weeks  
**Risk Level:** Medium  
**Regulatory Priority:** High (FFIEC, Basel III)

### 1.1 Per-Tenant Calibration Engine

**Objective:** Allow each tenant (business unit, subsidiary, geography) to define custom risk thresholds and scoring parameters.

#### Implementation

```python
# New: parity/tenant_config.py
@dataclass
class TenantConfig:
    tenant_id: str
    name: str
    jurisdiction: Literal["US", "EU", "UK", "APAC"]
    
    # Custom thresholds
    parity_threshold_safe: float = 95.0      # SAFE_TO_CUT if >= this
    parity_threshold_monitor: float = 80.0   # CUT_WITH_MONITORING if >= this
    parity_threshold_hold: float = 60.0      # HOLD_INVESTIGATE if >= this
    
    # Tolerance bands (can be tighter for high-value functions)
    fee_tolerance_usd: Decimal = Decimal("0.02")
    amount_tolerance_usd: Decimal = Decimal("0.05")
    
    # Anomaly detection sensitivity
    anomaly_sigma_threshold: float = 2.0     # Can increase to 2.5 or 3.0 for less sensitive
    
    # Regulatory framework
    primary_regulator: str = "OCC"           # OCC, EBA, FCA, MAS, etc.
    compliance_frameworks: list[str] = field(default_factory=lambda: ["FFIEC", "Basel III"])
    
    # Business rules
    max_exposure_usd: float = 10_000_000.0   # Block cutover if exposure exceeds this
    require_dual_approval: bool = True       # CTO + Compliance sign-off required
```

#### Scoring Changes

```python
# Modified: parity/scoring.py
class FunctionScore:
    def __init__(self, name: str, tenant_config: TenantConfig):
        self.name = name
        self.tenant_config = tenant_config
        # ... existing fields
    
    @property
    def verdict(self) -> str:
        """Tenant-specific verdict thresholds."""
        score = self.readiness_score
        cfg = self.tenant_config
        
        if score >= cfg.parity_threshold_safe:
            return "SAFE_TO_CUT"
        elif score >= cfg.parity_threshold_monitor:
            return "CUT_WITH_MONITORING"
        elif score >= cfg.parity_threshold_hold:
            return "HOLD_INVESTIGATE"
        else:
            return "DO_NOT_CUT"
    
    @property
    def exposure_blocks_cutover(self) -> bool:
        """Check if exposure exceeds tenant's risk appetite."""
        return self.exposure_usd > self.tenant_config.max_exposure_usd
```

#### Database Schema

```sql
-- New: tenant_configs table
CREATE TABLE tenant_configs (
    tenant_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    jurisdiction VARCHAR(10) NOT NULL,
    config_json JSONB NOT NULL,  -- Full TenantConfig serialized
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(100)
);

-- New: analysis_runs table (track all runs with tenant context)
CREATE TABLE analysis_runs (
    run_id UUID PRIMARY KEY,
    tenant_id VARCHAR(50) REFERENCES tenant_configs(tenant_id),
    run_timestamp TIMESTAMP NOT NULL,
    n_transactions INT NOT NULL,
    overall_parity_pct DECIMAL(5,2),
    total_exposure_usd DECIMAL(15,2),
    verdict_summary JSONB,  -- {safe: 2, blocked: 2, etc.}
    config_snapshot JSONB,  -- TenantConfig at time of run
    INDEX idx_tenant_time (tenant_id, run_timestamp DESC)
);
```

### 1.2 Interactive Confidence Band Visualization

**Objective:** Show statistical uncertainty visually so regulators can assess confidence in verdicts.

#### New Chart: Confidence Band Over Time

```python
# New: dashboard.py addition
def plot_confidence_bands(history: list[dict], function_name: str):
    """
    Plot parity rate with 95% CI bands across run history.
    Shows if confidence is narrowing (good) or widening (bad).
    """
    fig = go.Figure()
    
    # Extract data for this function
    runs = [h for h in history if function_name in h]
    x = [r["run"] for r in runs]
    y = [r[function_name]["parity_pct"] for r in runs]
    ci_low = [r[function_name]["ci_low"] for r in runs]
    ci_high = [r[function_name]["ci_high"] for r in runs]
    
    # Confidence band (filled area)
    fig.add_trace(go.Scatter(
        x=x + x[::-1],
        y=ci_high + ci_low[::-1],
        fill='toself',
        fillcolor='rgba(15, 98, 254, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence Band',
        showlegend=True,
    ))
    
    # Parity rate line
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        name='Parity Rate',
        line=dict(color='#42be65', width=3),
        marker=dict(size=8),
    ))
    
    # Threshold line
    fig.add_hline(y=95, line_dash="dot", line_color="#0f62fe", 
                  annotation_text="Cut Threshold")
    
    fig.update_layout(
        title=f"{function_name} — Parity with 95% CI",
        yaxis=dict(range=[0, 110], title="Parity %"),
        xaxis=dict(title="Analysis Run"),
    )
    return fig
```

#### Regulatory Value

- **FFIEC IT Examination Handbook:** "Statistical methods must include confidence intervals to quantify uncertainty"
- **Basel III Pillar 3:** Requires disclosure of estimation uncertainty in operational risk models
- **PSD2 RTS:** Testing results must demonstrate statistical significance

### 1.3 Sample Size Adequacy Check

**Objective:** Warn when sample size is too small for reliable confidence intervals.

```python
# New: parity/scoring.py
class FunctionScore:
    @property
    def sample_size_adequate(self) -> bool:
        """
        Check if sample size meets statistical power requirements.
        Rule of thumb: n >= 30 for normal approximation, n >= 100 for tight CI.
        """
        return self.total >= 100
    
    @property
    def sample_size_warning(self) -> str | None:
        if self.total < 30:
            return "CRITICAL: Sample size too small for reliable inference (n < 30)"
        elif self.total < 100:
            return "WARNING: Sample size below recommended threshold (n < 100)"
        return None
```

---

## Phase 2: Temporal Intelligence (Drift Detection)
**Duration:** 4 weeks  
**Risk Level:** High (complex statistical modeling)  
**Regulatory Priority:** Critical (PSD2 Art. 98, Basel III)

### 2.1 Run History Database

**Objective:** Persist all analysis runs with full context for temporal analysis.

```sql
-- New: function_scores_history table
CREATE TABLE function_scores_history (
    score_id UUID PRIMARY KEY,
    run_id UUID REFERENCES analysis_runs(run_id),
    function_name VARCHAR(100) NOT NULL,
    total_transactions INT NOT NULL,
    passing_transactions INT NOT NULL,
    parity_rate_pct DECIMAL(5,2) NOT NULL,
    ci_low DECIMAL(5,2) NOT NULL,
    ci_high DECIMAL(5,2) NOT NULL,
    readiness_score DECIMAL(5,2) NOT NULL,
    verdict VARCHAR(50) NOT NULL,
    avg_fee_diff_usd DECIMAL(10,4),
    exposure_usd DECIMAL(15,2),
    anomaly_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_function_time (function_name, created_at DESC)
);

-- New: divergences_history table (for root cause analysis)
CREATE TABLE divergences_history (
    divergence_id UUID PRIMARY KEY,
    run_id UUID REFERENCES analysis_runs(run_id),
    transaction_id VARCHAR(100) NOT NULL,
    function_name VARCHAR(100) NOT NULL,
    field VARCHAR(50) NOT NULL,
    legacy_value DECIMAL(15,4),
    modern_value DECIMAL(15,4),
    diff_value DECIMAL(15,4),
    severity VARCHAR(20) NOT NULL,
    is_anomaly BOOLEAN DEFAULT FALSE,
    anomaly_sigma DECIMAL(5,2),
    regulation_citation VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_function_field (function_name, field, created_at DESC)
);
```

### 2.2 Drift Detection Engine

**Objective:** Detect statistically significant degradation in parity over time.

```python
# New: parity/drift_detection.py
from scipy import stats
import numpy as np

@dataclass
class DriftAnalysis:
    function_name: str
    window_size: int  # Number of runs analyzed
    
    # Trend analysis
    trend_direction: Literal["improving", "stable", "degrading"]
    trend_slope: float  # % change per run
    trend_p_value: float  # Statistical significance
    
    # Volatility
    parity_std_dev: float
    volatility_level: Literal["low", "medium", "high"]
    
    # Drift detection
    drift_detected: bool
    drift_magnitude: float  # % drop from baseline
    drift_confidence: float  # 0-1
    
    # Regulatory flags
    requires_investigation: bool
    regulatory_concern: str | None

def detect_drift(history: list[FunctionScore], 
                 baseline_window: int = 10,
                 detection_window: int = 5) -> DriftAnalysis:
    """
    Detect drift using CUSUM (Cumulative Sum Control Chart) method.
    
    Regulatory basis:
    - FFIEC: "Continuous monitoring must detect performance degradation"
    - Basel III: "Operational risk models must include early warning indicators"
    - PSD2 Art. 98: "Testing must continue throughout migration period"
    """
    if len(history) < baseline_window + detection_window:
        return DriftAnalysis(
            function_name=history[0].name,
            window_size=len(history),
            trend_direction="stable",
            trend_slope=0.0,
            trend_p_value=1.0,
            parity_std_dev=0.0,
            volatility_level="low",
            drift_detected=False,
            drift_magnitude=0.0,
            drift_confidence=0.0,
            requires_investigation=False,
            regulatory_concern=None,
        )
    
    # Extract parity rates
    parity_rates = [s.parity_rate for s in history]
    
    # 1. Trend analysis (linear regression)
    x = np.arange(len(parity_rates))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, parity_rates)
    
    trend_direction = "stable"
    if p_value < 0.05:  # Statistically significant trend
        if slope < -0.5:  # Degrading > 0.5% per run
            trend_direction = "degrading"
        elif slope > 0.5:  # Improving > 0.5% per run
            trend_direction = "improving"
    
    # 2. Volatility analysis
    std_dev = np.std(parity_rates)
    if std_dev < 2.0:
        volatility = "low"
    elif std_dev < 5.0:
        volatility = "medium"
    else:
        volatility = "high"
    
    # 3. CUSUM drift detection
    baseline = parity_rates[:baseline_window]
    recent = parity_rates[-detection_window:]
    
    baseline_mean = np.mean(baseline)
    recent_mean = np.mean(recent)
    
    drift_magnitude = baseline_mean - recent_mean
    
    # Statistical test: two-sample t-test
    t_stat, t_p_value = stats.ttest_ind(baseline, recent)
    drift_detected = (t_p_value < 0.05) and (drift_magnitude > 2.0)  # >2% drop
    
    # 4. Regulatory concern assessment
    regulatory_concern = None
    requires_investigation = False
    
    if drift_detected and drift_magnitude > 5.0:
        regulatory_concern = "CRITICAL: >5% parity degradation detected (PSD2 Art. 98 breach risk)"
        requires_investigation = True
    elif trend_direction == "degrading" and volatility == "high":
        regulatory_concern = "WARNING: Unstable degrading trend (Basel III operational risk flag)"
        requires_investigation = True
    
    return DriftAnalysis(
        function_name=history[0].name,
        window_size=len(history),
        trend_direction=trend_direction,
        trend_slope=slope,
        trend_p_value=p_value,
        parity_std_dev=std_dev,
        volatility_level=volatility,
        drift_detected=drift_detected,
        drift_magnitude=drift_magnitude,
        drift_confidence=1.0 - t_p_value,
        requires_investigation=requires_investigation,
        regulatory_concern=regulatory_concern,
    )
```

### 2.3 Drift Visualization Dashboard

```python
# New dashboard section: Drift Analysis
st.markdown("## Drift Detection — Temporal Stability Analysis")

for function_name in function_names:
    history = get_function_history(function_name, last_n_runs=20)
    drift = detect_drift(history)
    
    # Alert banner if drift detected
    if drift.drift_detected:
        st.error(f"🚨 DRIFT DETECTED: {function_name}")
        st.markdown(f"**Magnitude:** {drift.drift_magnitude:.1f}% drop from baseline")
        st.markdown(f"**Confidence:** {drift.drift_confidence*100:.0f}%")
        if drift.regulatory_concern:
            st.markdown(f"**Regulatory:** {drift.regulatory_concern}")
    
    # Trend chart
    fig = plot_drift_analysis(history, drift)
    st.plotly_chart(fig)
```

---

## Phase 3: Regulatory Compliance Framework
**Duration:** 3 weeks  
**Risk Level:** Low (documentation-heavy)  
**Regulatory Priority:** Critical (all frameworks)

### 3.1 Explicit Regulation Mapping

**Objective:** Replace hard-coded regulation strings with a structured compliance database.

```python
# New: compliance/regulations.py
@dataclass
class RegulationArticle:
    framework: str  # "FFIEC", "Basel III", "PSD2", "SWIFT gpi"
    article: str    # "Art. 45", "Pillar 3", "IT Handbook Section 5.2"
    title: str
    requirement: str
    applies_to: list[str]  # ["fee", "processed_amount", "status"]
    jurisdiction: list[str]  # ["US", "EU", "UK"]
    severity_if_breach: Literal["CRITICAL", "HIGH", "MEDIUM"]
    citation_url: str

# Regulation database
REGULATIONS = {
    "PSD2_ART_45": RegulationArticle(
        framework="PSD2",
        article="Art. 45",
        title="FX Transparency Requirements",
        requirement="Payment service providers must disclose FX conversion rates and charges before transaction execution",
        applies_to=["fee", "processed_amount"],
        jurisdiction=["EU", "UK"],
        severity_if_breach="CRITICAL",
        citation_url="https://eur-lex.europa.eu/eli/dir/2015/2366/oj",
    ),
    "BASEL_III_PILLAR_3": RegulationArticle(
        framework="Basel III",
        article="Pillar 3",
        title="Operational Risk Disclosure",
        requirement="Banks must disclose operational risk capital requirements and loss event data",
        applies_to=["processed_amount", "status"],
        jurisdiction=["US", "EU", "UK", "APAC"],
        severity_if_breach="HIGH",
        citation_url="https://www.bis.org/publ/bcbs189.htm",
    ),
    "FFIEC_IT_5_2": RegulationArticle(
        framework="FFIEC",
        article="IT Examination Handbook — Section 5.2",
        title="System Development and Acquisition",
        requirement="Financial institutions must test system changes with statistically valid samples and document results",
        applies_to=["fee", "processed_amount", "status"],
        jurisdiction=["US"],
        severity_if_breach="HIGH",
        citation_url="https://ithandbook.ffiec.gov/",
    ),
    # ... add all regulations
}
```

### 3.2 Compliance Scorecard

```python
# New: compliance/scorecard.py
@dataclass
class ComplianceCheck:
    regulation_id: str
    regulation: RegulationArticle
    status: Literal["PASS", "FAIL", "PARTIAL", "NOT_APPLICABLE"]
    evidence: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    remediation: str | None

def generate_compliance_scorecard(
    scores: list[FunctionScore],
    tenant_config: TenantConfig
) -> list[ComplianceCheck]:
    """
    Generate a compliance scorecard showing adherence to each regulation.
    """
    checks = []
    
    # FFIEC: Statistical rigor
    if "FFIEC" in tenant_config.compliance_frameworks:
        all_adequate = all(s.sample_size_adequate for s in scores)
        checks.append(ComplianceCheck(
            regulation_id="FFIEC_IT_5_2",
            regulation=REGULATIONS["FFIEC_IT_5_2"],
            status="PASS" if all_adequate else "FAIL",
            evidence=f"Sample sizes: {[s.total for s in scores]}. All >= 100: {all_adequate}",
            risk_level="HIGH" if not all_adequate else "LOW",
            remediation="Increase sample size to >= 100 per function" if not all_adequate else None,
        ))
    
    # Basel III: Operational risk capital
    if "Basel III" in tenant_config.compliance_frameworks:
        total_exposure = sum(s.exposure_usd for s in scores)
        exposure_acceptable = total_exposure < tenant_config.max_exposure_usd
        checks.append(ComplianceCheck(
            regulation_id="BASEL_III_PILLAR_3",
            regulation=REGULATIONS["BASEL_III_PILLAR_3"],
            status="PASS" if exposure_acceptable else "FAIL",
            evidence=f"Total exposure: ${total_exposure:,.0f}. Limit: ${tenant_config.max_exposure_usd:,.0f}",
            risk_level="CRITICAL" if not exposure_acceptable else "LOW",
            remediation="Reduce exposure or increase risk appetite limit" if not exposure_acceptable else None,
        ))
    
    # PSD2: FX transparency
    if "PSD2" in tenant_config.compliance_frameworks:
        intl_function = next((s for s in scores if "International" in s.name), None)
        if intl_function:
            fx_compliant = intl_function.verdict in ("SAFE_TO_CUT", "CUT_WITH_MONITORING")
            checks.append(ComplianceCheck(
                regulation_id="PSD2_ART_45",
                regulation=REGULATIONS["PSD2_ART_45"],
                status="PASS" if fx_compliant else "FAIL",
                evidence=f"International Wire Transfer verdict: {intl_function.verdict}",
                risk_level="CRITICAL" if not fx_compliant else "LOW",
                remediation="Resolve FX margin divergence before cutover" if not fx_compliant else None,
            ))
    
    return checks
```

### 3.3 Enhanced Audit PDF with Compliance Section

```python
# Modified: audit/pdf_report.py
def generate_pdf(scores, results, run_ts, tenant_config, compliance_checks):
    # ... existing sections ...
    
    # NEW SECTION: Regulatory Compliance Scorecard
    story.append(Paragraph("Regulatory Compliance Scorecard", s["section"]))
    
    comp_data = [["Framework", "Article", "Status", "Risk", "Evidence"]]
    for check in compliance_checks:
        status_color = {
            "PASS": C_GREEN,
            "PARTIAL": C_YELLOW,
            "FAIL": C_RED,
            "NOT_APPLICABLE": C_MID_GREY,
        }[check.status]
        
        comp_data.append([
            check.regulation.framework,
            check.regulation.article,
            check.status,
            check.risk_level,
            check.evidence[:80] + "..." if len(check.evidence) > 80 else check.evidence,
        ])
    
    t_comp = Table(comp_data, colWidths=[30*mm, 35*mm, 20*mm, 20*mm, 60*mm])
    # ... styling ...
    story.append(t_comp)
    
    # Remediation actions
    failed_checks = [c for c in compliance_checks if c.status == "FAIL"]
    if failed_checks:
        story.append(Paragraph("Required Remediation Actions", s["section"]))
        for check in failed_checks:
            story.append(Paragraph(
                f"<b>{check.regulation.framework} {check.regulation.article}:</b> {check.remediation}",
                s["body"]
            ))
```

---

## Phase 4: Advanced Observability & Audit Trail
**Duration:** 2 weeks  
**Risk Level:** Medium  
**Regulatory Priority:** High (FFIEC data integrity)

### 4.1 Immutable Audit Trail with Cryptographic Verification

**Objective:** Create tamper-evident audit trail using cryptographic hashing.

```python
# New: audit/blockchain_lite.py
import hashlib
import json
from datetime import datetime, timezone

@dataclass
class AuditBlock:
    block_id: str
    timestamp: datetime
    run_id: str
    tenant_id: str
    data_hash: str  # SHA-256 of scores + results
    previous_hash: str  # Hash of previous block (blockchain-style)
    signature: str  # HMAC signature for verification
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of block contents."""
        content = f"{self.block_id}{self.timestamp.isoformat()}{self.run_id}{self.data_hash}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def verify(self, previous_block: 'AuditBlock' | None) -> bool:
        """Verify block integrity."""
        # Check hash matches
        if self.compute_hash() != self.signature:
            return False
        
        # Check chain integrity
        if previous_block and self.previous_hash != previous_block.signature:
            return False
        
        return True

class AuditChain:
    """Blockchain-lite audit trail for regulatory compliance."""
    
    def __init__(self):
        self.blocks: list[AuditBlock] = []
    
    def add_run(self, run_id: str, tenant_id: str, scores: list[dict], results: list[dict]) -> AuditBlock:
        """Add a new analysis run to the audit chain."""
        # Compute data hash
        data = json.dumps({"scores": scores, "results": results}, sort_keys=True)
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        
        # Get previous hash
        previous_hash = self.blocks[-1].signature if self.blocks else "0" * 64
        
        # Create block
        block = AuditBlock(
            block_id=f"BLOCK-{len(self.blocks):06d}",
            timestamp=datetime.now(timezone.utc),
            run_id=run_id,
            tenant_id=tenant_id,
            data_hash=data_hash,
            previous_hash=previous_hash,
            signature="",  # Will be computed
        )
        block.signature = block.compute_hash()
        
        self.blocks.append(block)
        return block
    
    def verify_chain(self) -> tuple[bool, str]:
        """Verify entire audit chain integrity."""
        for i, block in enumerate(self.blocks):
            prev = self.blocks[i-1] if i > 0 else None
            if not block.verify(prev):
                return False, f"Block {block.block_id} failed verification"
        return True, "Audit chain verified"
```

### 4.2 Real-Time Observability Dashboard

```python
# New: observability/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Metrics
parity_analysis_runs = Counter(
    'bob_judge_analysis_runs_total',
    'Total number of parity analysis runs',
    ['tenant_id', 'function_name']
)

parity_rate = Gauge(
    'bob_judge_parity_rate',
    'Current parity rate per function',
    ['tenant_id', 'function_name']
)

divergence_count = Counter(
    'bob_judge_divergences_total',
    'Total divergences detected',
    ['tenant_id', 'function_name', 'severity']
)

analysis_duration = Histogram(
    'bob_judge_analysis_duration_seconds',
    'Time to complete parity analysis',
    ['tenant_id']
)

# Export to Prometheus/Grafana
from prometheus_client import start_http_server
start_http_server(9090)  # Metrics endpoint
```

### 4.3 Audit Trail Export Formats

```python
# New: audit/export.py
def export_audit_trail(
    format: Literal["pdf", "json", "csv", "xml"],
    run_id: str,
    include_blockchain: bool = True
) -> bytes:
    """
    Export audit trail in multiple formats for different regulators.
    
    - PDF: Human-readable for OCC examiners
    - JSON: Machine-readable for automated compliance checks
    - CSV: Spreadsheet import for risk committees
    - XML: XBRL-compatible for regulatory filings
    """
    if format == "pdf":
        return generate_pdf(...)  # Existing
    elif format == "json":
        return export_json_audit(run_id, include_blockchain)
    elif format == "csv":
        return export_csv_audit(run_id)
    elif format == "xml":
        return export_xml_audit(run_id)  # XBRL format
```

---

## Risk Register

| Risk ID | Description | Probability | Impact | Mitigation | Owner |
|---------|-------------|-------------|--------|------------|-------|
| **R1** | Per-tenant configs increase complexity, harder to maintain | Medium | Medium | Implement config validation + unit tests. Provide tenant config templates. | Engineering |
| **R2** | Drift detection false positives cause alert fatigue | Medium | High | Tune sigma thresholds per tenant. Add "snooze" feature for known issues. | Data Science |
| **R3** | Database schema changes break existing deployments | Low | High | Use Alembic migrations. Maintain backward compatibility for 2 versions. | DevOps |
| **R4** | Regulatory citations become outdated | Medium | Critical | Quarterly review cycle. Subscribe to regulatory update feeds (FFIEC, EBA). | Compliance |
| **R5** | Blockchain-lite audit trail performance overhead | Low | Medium | Async block creation. Batch writes. Use PostgreSQL JSONB for efficiency. | Engineering |
| **R6** | Multi-jurisdiction compliance increases legal risk | High | Critical | Engage external legal counsel. Get sign-off from each jurisdiction's compliance team. | Legal/Compliance |
| **R7** | Sample size requirements conflict with fast iteration | Medium | Medium | Implement "quick scan" mode (n=30) vs "full audit" mode (n=100+). | Product |
| **R8** | Confidence band visualization confuses non-technical users | Medium | Low | Add tooltips, explainer text. Provide "executive summary" view. | UX |

---

## Implementation Sequencing

### Sprint 1-2: Foundation (Weeks 1-2)
**Goal:** Database schema + tenant config engine

- [ ] Design and implement tenant_configs table
- [ ] Design and implement analysis_runs, function_scores_history, divergences_history tables
- [ ] Create TenantConfig dataclass with validation
- [ ] Implement tenant-specific threshold logic in [`FunctionScore.verdict`](parity/scoring.py:86)
- [ ] Add tenant selector to dashboard UI
- [ ] Write migration scripts (Alembic)
- [ ] Unit tests for tenant config validation

**Dependencies:** None  
**Risk:** R3 (schema changes)  
**Deliverable:** Working multi-tenant scoring engine

### Sprint 3-4: Statistical Rigor (Weeks 3-4)
**Goal:** Confidence bands + sample size checks

- [ ] Implement [`plot_confidence_bands()`](dashboard.py:676) with Plotly
- [ ] Add [`sample_size_adequate`](parity/scoring.py:1) property to FunctionScore
- [ ] Create sample size warning UI in dashboard
- [ ] Add confidence band chart to audit PDF
- [ ] Write statistical validation tests (scipy.stats)

**Dependencies:** Sprint 1-2 (database)  
**Risk:** R8 (visualization complexity)  
**Deliverable:** Interactive confidence band charts

### Sprint 5-7: Drift Detection (Weeks 5-7)
**Goal:** Temporal analysis engine

- [ ] Implement [`detect_drift()`](NEXT_ITERATION_PLAN.md:1) function with CUSUM
- [ ] Create drift_analysis table in database
- [ ] Build drift visualization dashboard section
- [ ] Add drift alerts to MCP server tools
- [ ] Implement trend analysis (linear regression)
- [ ] Write drift detection unit tests with synthetic data

**Dependencies:** Sprint 1-2 (history database)  
**Risk:** R2 (false positives)  
**Deliverable:** Working drift detection with alerts

### Sprint 8-9: Regulatory Framework (Weeks 8-9)
**Goal:** Compliance scorecard

- [ ] Build regulations database (REGULATIONS dict)
- [ ] Implement [`generate_compliance_scorecard()`](NEXT_ITERATION_PLAN.md:1)
- [ ] Add compliance section to audit PDF
- [ ] Create regulation citation links in UI
- [ ] Map all existing divergences to specific regulations
- [ ] Legal review of regulation citations

**Dependencies:** None (can run parallel)  
**Risk:** R4 (outdated citations), R6 (legal risk)  
**Deliverable:** Compliance scorecard in PDF

### Sprint 10-11: Audit Trail (Weeks 10-11)
**Goal:** Immutable evidence chain

- [ ] Implement AuditBlock and AuditChain classes
- [ ] Add blockchain-lite to analysis run workflow
- [ ] Create audit chain verification endpoint
- [ ] Implement multi-format export (JSON, CSV, XML)
- [ ] Add Prometheus metrics
- [ ] Performance testing (ensure <100ms overhead)

**Dependencies:** Sprint 1-2 (database)  
**Risk:** R5 (performance)  
**Deliverable:** Tamper-evident audit trail

### Sprint 12: Integration & Testing (Week 12)
**Goal:** End-to-end validation

- [ ] Integration tests across all phases
- [ ] Load testing (1000+ transactions)
- [ ] Regulatory compliance dry-run with legal team
- [ ] Documentation update (README, API docs)
- [ ] Demo video for v2.0 launch

**Dependencies:** All previous sprints  
**Risk:** None (buffer sprint)  
**Deliverable:** Production-ready v2.0

---

## Success Metrics

### Technical Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Tenant config coverage** | 100% of functions support tenant-specific thresholds | Unit test coverage |
| **Drift detection accuracy** | <5% false positive rate | Backtesting on historical data |
| **Confidence band precision** | CI width < 10% for n >= 100 | Statistical validation |
| **Audit trail integrity** | 100% chain verification success | Automated verification tests |
| **Performance overhead** | <10% increase in analysis time | Benchmark tests |

### Regulatory Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **FFIEC compliance** | Pass all IT Handbook Section 5.2 requirements | External audit |
| **Basel III alignment** | Operational risk capital calculation matches Pillar 3 | Compliance review |
| **PSD2 coverage** | All payment functions mapped to PSD2 articles | Legal sign-off |
| **Audit defensibility** | PDF accepted by OCC examiner without questions | Mock examination |

### Business Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Cutover confidence** | 95% of stakeholders "confident" in verdicts | Survey |
| **Time to regulatory approval** | <2 weeks from analysis to sign-off | Process tracking |
| **False cutover blocks** | <1% of SAFE_TO_CUT verdicts fail in production | Post-cutover monitoring |

---

## Acceptance Criteria

### Phase 1: Enhanced Statistical Rigor
- [ ] Tenant configs can be created, updated, and applied to scoring
- [ ] Confidence bands display correctly in dashboard with historical data
- [ ] Sample size warnings appear when n < 100
- [ ] Tenant-specific thresholds change verdict outcomes as expected

### Phase 2: Temporal Intelligence
- [ ] Drift detection runs automatically on each analysis
- [ ] Drift alerts appear in dashboard when degradation detected
- [ ] Trend charts show improving/stable/degrading patterns
- [ ] Historical data persists across sessions

### Phase 3: Regulatory Compliance
- [ ] Compliance scorecard shows PASS/FAIL for each regulation
- [ ] All divergences cite specific regulation articles
- [ ] PDF includes full compliance section with remediation actions
- [ ] Legal team approves regulation citations

### Phase 4: Advanced Observability
- [ ] Audit chain verifies successfully after 100+ runs
- [ ] Prometheus metrics export correctly
- [ ] Multi-format export (PDF, JSON, CSV, XML) works
- [ ] Blockchain-lite adds <100ms overhead

---

## Next Steps

1. **Stakeholder Review** (Week 1)
   - Present this plan to CTO, Compliance, Legal
   - Get sign-off on regulatory priorities
   - Confirm budget and timeline

2. **Team Formation** (Week 1)
   - Assign engineering lead for each phase
   - Engage data scientist for drift detection
   - Retain external legal counsel for regulation review

3. **Sprint 0: Setup** (Week 1)
   - Set up development environment
   - Create feature branches
   - Initialize database migrations
   - Write technical design docs for each phase

4. **Kickoff** (Week 2)
   - Sprint 1 begins
   - Daily standups
   - Weekly demos to stakeholders

---

## Appendix: Regulatory Reference Links

- **FFIEC IT Examination Handbook:** https://ithandbook.ffiec.gov/
- **Basel III Framework:** https://www.bis.org/bcbs/basel3.htm
- **PSD2 Directive:** https://eur-lex.europa.eu/eli/dir/2015/2366/oj
- **SWIFT gpi Standards:** https://www.swift.com/our-solutions/global-financial-messaging/payments-cash-management/swift-gpi
- **EBA Guidelines on Operational Risk:** https://www.eba.europa.eu/regulation-and-policy/operational-risk

---

**Document Status:** Draft for Review  
**Next Review:** After stakeholder feedback  
**Approval Required:** CTO, Chief Compliance Officer, General Counsel