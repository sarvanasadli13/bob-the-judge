**User:**

<task>
Review the current state of this project:
  - parity/tenant_config.py
  - parity/confidence.py
  - parity/drift_detection.py
  - parity/compliance.py
  - dashboard.py
  - mcp_server.py
  - audit/pdf_report.py

  Do a code review without making changes. Identify:
  1. Any obvious bugs or edge cases not handled
  2. Integration risks (do new modules interact safely with old code?)
  3. Missing test coverage
  4. Anything that would worry a regulator reviewer
  5. Anything that could break in production / Railway deployment

  Output a short prioritized list of findings (CRITICAL / HIGH / MEDIUM /
  LOW). Do not modify any files.
</task>
<environment_details>
# VSCode Visible Files
dashboard.py

# VSCode Open Tabs
parity/tenant_config.py,config/tenants.json,parity/parity_engine.py,parity/scoring.py,dashboard.py,parity/confidence.py,parity/drift_detection.py,parity/compliance.py,mcp_server.py,audit/pdf_report.py,ENHANCEMENT_GUIDE.md,tests/test_tenant_config.py,tests/test_confidence.py,tests/test_drift_detection.py,tests/__init__.py,requirements.txt,tests/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-15T18:04:23.317Z
User time zone: Europe/Berlin, UTC+2:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (c:/Users/Sarvan/projects/bob-the-judge) Files
.gitignore
1.0
2sigma)
audit_demo.pdf
audit_test.pdf
Bob_the_Judge_Pitch_Deck.pptx
bob-mcp-config.json
BobTheJudge.exe
build_deck.py
cover.jpg
dashboard.py
DEMO_SCRIPT.md
ENHANCEMENT_GUIDE.md
launch.py
LICENSE
mcp_server.py
Opening
PITCH_SCRIPTS.md
railway.toml
README.md
requirements.txt
run_services.bat
session6_transcript.txt
Showing
start.bat
start.sh
str
TenantProfile
test_parity.py
test_pdf.py
.pytest_cache/
assets/
assets/gavel.svg
audit/
audit/__init__.py
audit/pdf_report.py
bob/
bob/__init__.py
bob/client.py
bob_sessions/
bob_sessions/A_plan_consumption.png
bob_sessions/A_plan_v2enhanced.md
bob_sessions/A_plan.md
bob_sessions/B_code_consumption.png
bob_sessions/B_code.md
bob_sessions/C_ask_consumption.png
bob_sessions/C_ask.md
bob_sessions/D_orchestrato_sum.md
bob_sessions/D_orchestrator_consumption.png
bob_sessions/D_orchestrator1.md
bob_sessions/D_orchestrator2.md
bob_sessions/D_orchestrator3.md
bob_sessions/D_orchestrator4.md
bob_sessions/PROMPTS_TO_PASTE.md
bob_sessions/README.md
config/
config/tenants.json
docs/
docs/screenshots/
docs/screenshots/01-hero.png
docs/screenshots/02-results.png
docs/screenshots/03-ready-cutover.png
docs/screenshots/04-bob-code-fix.png
parity/
parity/__init__.py
parity/compliance.py
parity/confidence.py
parity/drift_detection.py
parity/parity_engine.py
parity/scoring.py
parity/tenant_config.py
parity/traffic_generator.py
services/
services/__init__.py
services/legacy_bank.py
services/models.py
services/modern_bank.py
services/cobol/
services/cobol/FEE_CALC.cob
tests/
tests/__init__.py
tests/README.md
tests/test_confidence.py
tests/test_drift_detection.py
tests/test_tenant_config.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll conduct a comprehensive code review of the specified files to identify potential issues, risks, and areas of concern.

<read_file>
<args>
  <file>
    <path>parity/tenant_config.py</path>
  </file>
  <file>
    <path>parity/confidence.py</path>
  </file>
  <file>
    <path>parity/drift_detection.py</path>
  </file>
  <file>
    <path>parity/compliance.py</path>
  </file>
  <file>
    <path>dashboard.py</path>
  </file>
</args>
</read_file>

<read_file>
<args>
  <file>
    <path>mcp_server.py</path>
  </file>
  <file>
    <path>audit/pdf_report.py</path>
  </file>
</args>
</read_file>

<read_file>
<args>
  <file>
    <path>p

[Response interrupted by a tool use result. Only one tool may be used at a time and should be placed at the end of the message.]

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>parity/tenant_config.py</path>
<content lines="1-158">
  1 | """
  2 | Tenant-specific parity thresholds and regulatory requirements.
  3 | 
  4 | Enables different banks to use risk-appropriate tolerances based on:
  5 | - Institution size (FFIEC categorization)
  6 | - Regulatory requirements (Basel III, PSD2)
  7 | - Risk appetite and operational complexity
  8 | 
  9 | Regulatory Basis:
 10 | - FFIEC IT Handbook: "Risk management practices should be commensurate with 
 11 |   the size, complexity, and risk profile of the institution"
 12 | - Basel III Pillar 2: Supervisory review requires institution-specific risk assessment
 13 | """
 14 | 
 15 | from dataclasses import dataclass
 16 | from decimal import Decimal
 17 | from typing import Literal
 18 | import json
 19 | from pathlib import Path
 20 | 
 21 | 
 22 | @dataclass
 23 | class TenantProfile:
 24 |     """
 25 |     Tenant-specific parity thresholds and regulatory requirements.
 26 |     Allows different banks to use risk-appropriate tolerances.
 27 |     """
 28 |     tenant_id: str
 29 |     name: str
 30 |     tier: Literal["tier1", "tier2", "community"]
 31 |     
 32 |     # Parity tolerances
 33 |     fee_tolerance_usd: Decimal
 34 |     amount_tolerance_usd: Decimal
 35 |     parity_threshold_pct: float  # Minimum parity rate for SAFE_TO_CUT
 36 |     
 37 |     # Anomaly detection
 38 |     anomaly_sigma_threshold: float  # Standard deviations for flagging
 39 |     
 40 |     # Regulatory context
 41 |     ffiec_category: str  # "Large Bank" / "Regional Bank" / "Community Bank"
 42 |     basel_operational_risk_weight: float  # 0.12 (12%) for tier1, 0.15 for tier2
 43 |     psd2_jurisdiction: bool
 44 |     
 45 |     # Risk appetite
 46 |     max_daily_exposure_usd: float
 47 |     requires_cto_signoff: bool
 48 |     
 49 |     def to_dict(self) -> dict:
 50 |         """Convert to dictionary for JSON serialization and API responses."""
 51 |         return {
 52 |             "tenant_id": self.tenant_id,
 53 |             "name": self.name,
 54 |             "tier": self.tier,
 55 |             "fee_tolerance_usd": float(self.fee_tolerance_usd),
 56 |             "amount_tolerance_usd": float(self.amount_tolerance_usd),
 57 |             "parity_threshold_pct": self.parity_threshold_pct,
 58 |             "anomaly_sigma_threshold": self.anomaly_sigma_threshold,
 59 |             "ffiec_category": self.ffiec_category,
 60 |             "basel_operational_risk_weight": self.basel_operational_risk_weight,
 61 |             "psd2_jurisdiction": self.psd2_jurisdiction,
 62 |             "max_daily_exposure_usd": self.max_daily_exposure_usd,
 63 |             "requires_cto_signoff": self.requires_cto_signoff,
 64 |         }
 65 | 
 66 | 
 67 | def load_tenant(tenant_id: str) -> TenantProfile:
 68 |     """
 69 |     Load tenant profile from config/tenants.json.
 70 |     
 71 |     Args:
 72 |         tenant_id: Unique tenant identifier (e.g., 'tier1_global', 'community_bank')
 73 |     
 74 |     Returns:
 75 |         TenantProfile with all configuration parameters
 76 |     
 77 |     Raises:
 78 |         ValueError: If tenant_id not found in configuration
 79 |         FileNotFoundError: If config/tenants.json doesn't exist
 80 |     """
 81 |     config_path = Path(__file__).parent.parent / "config" / "tenants.json"
 82 |     
 83 |     if not config_path.exists():
 84 |         raise FileNotFoundError(
 85 |             f"Tenant configuration not found at {config_path}. "
 86 |             "Please create config/tenants.json with tenant profiles."
 87 |         )
 88 |     
 89 |     with open(config_path) as f:
 90 |         tenants = json.load(f)
 91 |     
 92 |     if tenant_id not in tenants:
 93 |         available = ", ".join(tenants.keys())
 94 |         raise ValueError(
 95 |             f"Tenant '{tenant_id}' not found in config. "
 96 |             f"Available tenants: {available}"
 97 |         )
 98 |     
 99 |     data = tenants[tenant_id]
100 |     return TenantProfile(
101 |         tenant_id=tenant_id,
102 |         name=data["name"],
103 |         tier=data["tier"],
104 |         fee_tolerance_usd=Decimal(str(data["fee_tolerance_usd"])),
105 |         amount_tolerance_usd=Decimal(str(data["amount_tolerance_usd"])),
106 |         parity_threshold_pct=data["parity_threshold_pct"],
107 |         anomaly_sigma_threshold=data["anomaly_sigma_threshold"],
108 |         ffiec_category=data["ffiec_category"],
109 |         basel_operational_risk_weight=data["basel_operational_risk_weight"],
110 |         psd2_jurisdiction=data["psd2_jurisdiction"],
111 |         max_daily_exposure_usd=data["max_daily_exposure_usd"],
112 |         requires_cto_signoff=data["requires_cto_signoff"],
113 |     )
114 | 
115 | 
116 | def list_tenants() -> list[str]:
117 |     """
118 |     List all available tenant profile IDs.
119 | 
120 |     Returns:
121 |         List of tenant_id strings for each configured tenant
122 |     """
123 |     config_path = Path(__file__).parent.parent / "config" / "tenants.json"
124 | 
125 |     if not config_path.exists():
126 |         return []
127 | 
128 |     with open(config_path) as f:
129 |         tenants = json.load(f)
130 | 
131 |     return list(tenants.keys())
132 | 
133 | 
134 | def get_default_tenant() -> TenantProfile:
135 |     """
136 |     Get default tenant profile for backward compatibility.
137 |     Uses 'demo_default' if available, otherwise creates a standard tier2 profile.
138 |     """
139 |     try:
140 |         return load_tenant("demo_default")
141 |     except (FileNotFoundError, ValueError):
142 |         # Fallback to hardcoded tier2 defaults
143 |         return TenantProfile(
144 |             tenant_id="default",
145 |             name="Default Profile",
146 |             tier="tier2",
147 |             fee_tolerance_usd=Decimal("0.02"),
148 |             amount_tolerance_usd=Decimal("0.05"),
149 |             parity_threshold_pct=95.0,
150 |             anomaly_sigma_threshold=2.0,
151 |             ffiec_category="Regional Bank",
152 |             basel_operational_risk_weight=0.15,
153 |             psd2_jurisdiction=True,
154 |             max_daily_exposure_usd=5000000.0,
155 |             requires_cto_signoff=False,
156 |         )
157 | 
158 | # Made with Bob
</content>
</file>
<file><path>parity/confidence.py</path>
<content lines="1-277">
  1 | """
  2 | Advanced confidence interval methods for parity scoring.
  3 | 
  4 | Beyond Wilson 95% CI, provides:
  5 | - Bootstrap confidence intervals (resampling-based)
  6 | - Bayesian credible intervals (prior-informed)
  7 | - Funnel plot boundaries for small-sample detection
  8 | 
  9 | Regulatory Justification:
 10 | - FDA Guidance: "Multiple methods strengthen statistical inference"
 11 | - Basel III: "Model validation requires sensitivity analysis"
 12 | - FFIEC: "Risk assessment should use multiple analytical approaches"
 13 | """
 14 | 
 15 | import numpy as np
 16 | from typing import Tuple, List
 17 | from dataclasses import dataclass
 18 | 
 19 | 
 20 | @dataclass
 21 | class ConfidenceInterval:
 22 |     """Container for confidence interval results."""
 23 |     method: str
 24 |     lower: float
 25 |     upper: float
 26 |     point_estimate: float
 27 |     confidence_level: float
 28 |     
 29 |     def width(self) -> float:
 30 |         """Return the width of the confidence interval."""
 31 |         return self.upper - self.lower
 32 |     
 33 |     def contains(self, value: float) -> bool:
 34 |         """Check if a value falls within the interval."""
 35 |         return self.lower <= value <= self.upper
 36 | 
 37 | 
 38 | def wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> ConfidenceInterval:
 39 |     """
 40 |     Wilson score confidence interval (current method).
 41 |     
 42 |     More accurate than normal approximation for small samples and extreme proportions.
 43 |     Used as baseline for comparison with other methods.
 44 |     
 45 |     Args:
 46 |         successes: Number of successful comparisons (parity matches)
 47 |         trials: Total number of comparisons
 48 |         confidence: Confidence level (default 0.95 for 95% CI)
 49 |     
 50 |     Returns:
 51 |         ConfidenceInterval with Wilson score bounds
 52 |     """
 53 |     if trials == 0:
 54 |         return ConfidenceInterval("wilson", 0.0, 0.0, 0.0, confidence)
 55 |     
 56 |     p = successes / trials
 57 |     z = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%
 58 |     
 59 |     denominator = 1 + z**2 / trials
 60 |     center = (p + z**2 / (2 * trials)) / denominator
 61 |     margin = z * np.sqrt((p * (1 - p) / trials + z**2 / (4 * trials**2))) / denominator
 62 |     
 63 |     lower = max(0.0, center - margin)
 64 |     upper = min(1.0, center + margin)
 65 |     
 66 |     return ConfidenceInterval("wilson", lower * 100, upper * 100, p * 100, confidence)
 67 | 
 68 | 
 69 | def bootstrap_interval(successes: int, trials: int, confidence: float = 0.95, n_bootstrap: int = 10000) -> ConfidenceInterval:
 70 |     """
 71 |     Bootstrap confidence interval using resampling.
 72 |     
 73 |     Non-parametric method that doesn't assume normal distribution.
 74 |     Particularly useful for small samples or skewed distributions.
 75 |     
 76 |     Regulatory Basis:
 77 |     - FDA: "Bootstrap methods provide robust uncertainty quantification"
 78 |     - Basel III: "Resampling techniques validate model assumptions"
 79 |     
 80 |     Args:
 81 |         successes: Number of successful comparisons
 82 |         trials: Total number of comparisons
 83 |         confidence: Confidence level (default 0.95)
 84 |         n_bootstrap: Number of bootstrap samples (default 10000)
 85 |     
 86 |     Returns:
 87 |         ConfidenceInterval with bootstrap percentile bounds
 88 |     """
 89 |     if trials == 0:
 90 |         return ConfidenceInterval("bootstrap", 0.0, 0.0, 0.0, confidence)
 91 |     
 92 |     # Create binary array: 1 for success, 0 for failure
 93 |     data = np.array([1] * successes + [0] * (trials - successes))
 94 |     
 95 |     # Bootstrap resampling
 96 |     bootstrap_means = []
 97 |     rng = np.random.default_rng(42)  # Fixed seed for reproducibility
 98 |     
 99 |     for _ in range(n_bootstrap):
100 |         sample = rng.choice(data, size=trials, replace=True)
101 |         bootstrap_means.append(np.mean(sample))
102 |     
103 |     # Percentile method
104 |     alpha = (1 - confidence) / 2
105 |     lower = float(np.percentile(bootstrap_means, alpha * 100))
106 |     upper = float(np.percentile(bootstrap_means, (1 - alpha) * 100))
107 |     point = successes / trials
108 |     
109 |     return ConfidenceInterval("bootstrap", lower * 100, upper * 100, point * 100, confidence)
110 | 
111 | 
112 | def bayesian_credible_interval(successes: int, trials: int, confidence: float = 0.95, 
113 |                                 prior_alpha: float = 1.0, prior_beta: float = 1.0) -> ConfidenceInterval:
114 |     """
115 |     Bayesian credible interval using Beta-Binomial conjugate prior.
116 |     
117 |     Incorporates prior knowledge about parity rates. Default uniform prior (α=1, β=1).
118 |     For banking: could use informative prior based on historical migration data.
119 |     
120 |     Regulatory Basis:
121 |     - Basel III Pillar 2: "Prior experience should inform risk assessment"
122 |     - FFIEC: "Historical performance data strengthens analysis"
123 |     
124 |     Args:
125 |         successes: Number of successful comparisons
126 |         trials: Total number of comparisons
127 |         confidence: Confidence level (default 0.95)
128 |         prior_alpha: Beta prior α parameter (default 1.0 = uniform)
129 |         prior_beta: Beta prior β parameter (default 1.0 = uniform)
130 |     
131 |     Returns:
132 |         ConfidenceInterval with Bayesian credible interval bounds
133 |     """
134 |     if trials == 0:
135 |         return ConfidenceInterval("bayesian", 0.0, 0.0, 0.0, confidence)
136 |     
137 |     # Posterior parameters (Beta distribution)
138 |     posterior_alpha = prior_alpha + successes
139 |     posterior_beta = prior_beta + (trials - successes)
140 |     
141 |     # Credible interval using Beta quantiles
142 |     from scipy.stats import beta
143 |     alpha = (1 - confidence) / 2
144 |     lower = float(beta.ppf(alpha, posterior_alpha, posterior_beta))
145 |     upper = float(beta.ppf(1 - alpha, posterior_alpha, posterior_beta))
146 |     
147 |     # Posterior mean (point estimate)
148 |     point = posterior_alpha / (posterior_alpha + posterior_beta)
149 |     
150 |     return ConfidenceInterval("bayesian", lower * 100, upper * 100, point * 100, confidence)
151 | 
152 | 
153 | def funnel_plot_bounds(n: int, target_rate: float = 95.0, confidence: float = 0.95) -> Tuple[float, float]:
154 |     """
155 |     Calculate funnel plot control limits for detecting outliers.
156 |     
157 |     Funnel plots show expected variation around a target rate as sample size changes.
158 |     Useful for identifying functions with unexpectedly low parity despite small samples.
159 |     
160 |     Regulatory Basis:
161 |     - FFIEC: "Statistical process control for operational risk monitoring"
162 |     - Basel III: "Outlier detection in operational loss data"
163 |     
164 |     Args:
165 |         n: Sample size (number of transactions)
166 |         target_rate: Target parity rate percentage (default 95%)
167 |         confidence: Confidence level for control limits (default 0.95)
168 |     
169 |     Returns:
170 |         Tuple of (lower_bound, upper_bound) in percentage
171 |     """
172 |     if n == 0:
173 |         return (0.0, 100.0)
174 |     
175 |     p = target_rate / 100
176 |     z = 1.96 if confidence == 0.95 else 2.576
177 |     
178 |     # Standard error for binomial proportion
179 |     se = np.sqrt(p * (1 - p) / n)
180 |     
181 |     lower = max(0.0, (p - z * se) * 100)
182 |     upper = min(100.0, (p + z * se) * 100)
183 |     
184 |     return (lower, upper)
185 | 
186 | 
187 | def compare_intervals(successes: int, trials: int, confidence: float = 0.95) -> dict:
188 |     """
189 |     Compare all confidence interval methods for a given dataset.
190 |     
191 |     Returns a dictionary with all methods for visualization and analysis.
192 |     Useful for understanding method sensitivity and robustness.
193 |     
194 |     Args:
195 |         successes: Number of successful comparisons
196 |         trials: Total number of comparisons
197 |         confidence: Confidence level (default 0.95)
198 |     
199 |     Returns:
200 |         Dictionary with all interval methods and comparison metrics
201 |     """
202 |     wilson = wilson_score_interval(successes, trials, confidence)
203 |     bootstrap = bootstrap_interval(successes, trials, confidence)
204 |     bayesian = bayesian_credible_interval(successes, trials, confidence)
205 |     funnel_lower, funnel_upper = funnel_plot_bounds(trials, 95.0, confidence)
206 |     
207 |     return {
208 |         "wilson": {
209 |             "lower": wilson.lower,
210 |             "upper": wilson.upper,
211 |             "point": wilson.point_estimate,
212 |             "width": wilson.width(),
213 |         },
214 |         "bootstrap": {
215 |             "lower": bootstrap.lower,
216 |             "upper": bootstrap.upper,
217 |             "point": bootstrap.point_estimate,
218 |             "width": bootstrap.width(),
219 |         },
220 |         "bayesian": {
221 |             "lower": bayesian.lower,
222 |             "upper": bayesian.upper,
223 |             "point": bayesian.point_estimate,
224 |             "width": bayesian.width(),
225 |         },
226 |         "funnel": {
227 |             "lower": funnel_lower,
228 |             "upper": funnel_upper,
229 |             "target": 95.0,
230 |         },
231 |         "sample_size": trials,
232 |         "successes": successes,
233 |         "confidence_level": confidence,
234 |     }
235 | 
236 | 
237 | def get_interval_consensus(successes: int, trials: int, confidence: float = 0.95) -> dict:
238 |     """
239 |     Get consensus view across all confidence interval methods.
240 |     
241 |     Provides a robust assessment by considering agreement across methods.
242 |     Flags cases where methods disagree significantly (model uncertainty).
243 |     
244 |     Args:
245 |         successes: Number of successful comparisons
246 |         trials: Total number of comparisons
247 |         confidence: Confidence level (default 0.95)
248 |     
249 |     Returns:
250 |         Dictionary with consensus metrics and disagreement flags
251 |     """
252 |     intervals = compare_intervals(successes, trials, confidence)
253 |     
254 |     # Extract lower and upper bounds from each method
255 |     lowers = [intervals["wilson"]["lower"], intervals["bootstrap"]["lower"], intervals["bayesian"]["lower"]]
256 |     uppers = [intervals["wilson"]["upper"], intervals["bootstrap"]["upper"], intervals["bayesian"]["upper"]]
257 |     
258 |     # Consensus: most conservative (widest) interval
259 |     consensus_lower = min(lowers)
260 |     consensus_upper = max(uppers)
261 |     
262 |     # Check for significant disagreement (>5% difference in bounds)
263 |     lower_range = max(lowers) - min(lowers)
264 |     upper_range = max(uppers) - min(uppers)
265 |     significant_disagreement = lower_range > 5.0 or upper_range > 5.0
266 |     
267 |     return {
268 |         "consensus_lower": consensus_lower,
269 |         "consensus_upper": consensus_upper,
270 |         "consensus_width": consensus_upper - consensus_lower,
271 |         "methods_agree": not significant_disagreement,
272 |         "lower_range": lower_range,
273 |         "upper_range": upper_range,
274 |         "all_intervals": intervals,
275 |     }
276 | 
277 | # Made with Bob
</content>
</file>
<file><path>parity/drift_detection.py</path>
<content lines="1-367">
  1 | """
  2 | Drift detection for monitoring parity degradation over time.
  3 | 
  4 | Implements statistical process control (SPC) methods:
  5 | - CUSUM (Cumulative Sum) for detecting sustained shifts
  6 | - EWMA (Exponentially Weighted Moving Average) for trend detection
  7 | - Run history tracking with SQLite persistence
  8 | 
  9 | Regulatory Justification:
 10 | - FFIEC: "Ongoing monitoring of operational risk indicators"
 11 | - Basel III: "Continuous assessment of operational risk exposure"
 12 | - PSD2: "Regular monitoring of payment service quality"
 13 | """
 14 | 
 15 | import sqlite3
 16 | from datetime import datetime, timezone
 17 | from pathlib import Path
 18 | from typing import List, Dict, Optional, Tuple
 19 | from dataclasses import dataclass, asdict
 20 | import json
 21 | 
 22 | 
 23 | @dataclass
 24 | class RunRecord:
 25 |     """Single analysis run record for drift tracking."""
 26 |     run_id: str
 27 |     timestamp: datetime
 28 |     tenant_id: str
 29 |     function_name: str
 30 |     parity_rate_pct: float
 31 |     total_transactions: int
 32 |     anomaly_count: int
 33 |     avg_fee_diff_usd: float
 34 |     verdict: str
 35 |     
 36 |     def to_dict(self) -> dict:
 37 |         """Convert to dictionary for JSON serialization."""
 38 |         d = asdict(self)
 39 |         d['timestamp'] = self.timestamp.isoformat()
 40 |         return d
 41 | 
 42 | 
 43 | class DriftDetector:
 44 |     """
 45 |     Detects drift in parity rates using statistical process control methods.
 46 |     
 47 |     Tracks historical runs and flags when parity degrades beyond expected variation.
 48 |     """
 49 |     
 50 |     def __init__(self, db_path: str = "data/run_history.db"):
 51 |         """
 52 |         Initialize drift detector with SQLite database.
 53 |         
 54 |         Args:
 55 |             db_path: Path to SQLite database file
 56 |         """
 57 |         self.db_path = Path(db_path)
 58 |         self.db_path.parent.mkdir(parents=True, exist_ok=True)
 59 |         self._init_db()
 60 |     
 61 |     def _init_db(self):
 62 |         """Create database tables if they don't exist."""
 63 |         conn = sqlite3.connect(self.db_path)
 64 |         cursor = conn.cursor()
 65 |         
 66 |         cursor.execute("""
 67 |             CREATE TABLE IF NOT EXISTS run_history (
 68 |                 id INTEGER PRIMARY KEY AUTOINCREMENT,
 69 |                 run_id TEXT NOT NULL,
 70 |                 timestamp TEXT NOT NULL,
 71 |                 tenant_id TEXT NOT NULL,
 72 |                 function_name TEXT NOT NULL,
 73 |                 parity_rate_pct REAL NOT NULL,
 74 |                 total_transactions INTEGER NOT NULL,
 75 |                 anomaly_count INTEGER NOT NULL,
 76 |                 avg_fee_diff_usd REAL NOT NULL,
 77 |                 verdict TEXT NOT NULL,
 78 |                 UNIQUE(run_id, function_name, tenant_id)
 79 |             )
 80 |         """)
 81 |         
 82 |         cursor.execute("""
 83 |             CREATE INDEX IF NOT EXISTS idx_function_time 
 84 |             ON run_history(function_name, timestamp)
 85 |         """)
 86 |         
 87 |         cursor.execute("""
 88 |             CREATE INDEX IF NOT EXISTS idx_tenant_function 
 89 |             ON run_history(tenant_id, function_name)
 90 |         """)
 91 |         
 92 |         conn.commit()
 93 |         conn.close()
 94 |     
 95 |     def record_run(self, run_id: str, tenant_id: str, scores: List[dict]):
 96 |         """
 97 |         Record a complete analysis run to history.
 98 |         
 99 |         Args:
100 |             run_id: Unique identifier for this run
101 |             tenant_id: Tenant profile used for analysis
102 |             scores: List of function scores from scoring module
103 |         """
104 |         conn = sqlite3.connect(self.db_path)
105 |         cursor = conn.cursor()
106 |         
107 |         timestamp = datetime.now(timezone.utc).isoformat()
108 |         
109 |         for score in scores:
110 |             cursor.execute("""
111 |                 INSERT INTO run_history 
112 |                 (run_id, timestamp, tenant_id, function_name, parity_rate_pct, 
113 |                  total_transactions, anomaly_count, avg_fee_diff_usd, verdict)
114 |                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
115 |             """, (
116 |                 run_id,
117 |                 timestamp,
118 |                 tenant_id,
119 |                 score['function'],
120 |                 score['parity_rate_pct'],
121 |                 score['total_transactions'],
122 |                 score.get('anomaly_count', 0),
123 |                 score['avg_fee_diff_usd'],
124 |                 score['verdict']
125 |             ))
126 |         
127 |         conn.commit()
128 |         conn.close()
129 |     
130 |     def get_history(self, function_name: str, tenant_id: Optional[str] = None, 
131 |                     limit: int = 100) -> List[RunRecord]:
132 |         """
133 |         Retrieve historical runs for a function.
134 |         
135 |         Args:
136 |             function_name: Payment function to query
137 |             tenant_id: Optional tenant filter
138 |             limit: Maximum number of records to return
139 |         
140 |         Returns:
141 |             List of RunRecord objects, newest first
142 |         """
143 |         conn = sqlite3.connect(self.db_path)
144 |         cursor = conn.cursor()
145 |         
146 |         cols = "run_id, timestamp, tenant_id, function_name, parity_rate_pct, total_transactions, anomaly_count, avg_fee_diff_usd, verdict"
147 |         if tenant_id:
148 |             cursor.execute(f"""
149 |                 SELECT {cols} FROM run_history
150 |                 WHERE function_name = ? AND tenant_id = ?
151 |                 ORDER BY timestamp DESC
152 |                 LIMIT ?
153 |             """, (function_name, tenant_id, limit))
154 |         else:
155 |             cursor.execute(f"""
156 |                 SELECT {cols} FROM run_history
157 |                 WHERE function_name = ?
158 |                 ORDER BY timestamp DESC
159 |                 LIMIT ?
160 |             """, (function_name, limit))
161 |         
162 |         rows = cursor.fetchall()
163 |         conn.close()
164 |         
165 |         records = []
166 |         for row in rows:
167 |             records.append(RunRecord(
168 |                 run_id=row[0],
169 |                 timestamp=datetime.fromisoformat(row[1]),
170 |                 tenant_id=row[2],
171 |                 function_name=row[3],
172 |                 parity_rate_pct=row[4],
173 |                 total_transactions=row[5],
174 |                 anomaly_count=row[6],
175 |                 avg_fee_diff_usd=row[7],
176 |                 verdict=row[8]
177 |             ))
178 |         
179 |         return records
180 |     
181 |     def cusum_detect(self, function_name: str, tenant_id: str, 
182 |                      target_rate: float = 95.0, threshold: float = 5.0) -> Dict:
183 |         """
184 |         CUSUM (Cumulative Sum) drift detection.
185 |         
186 |         Detects sustained shifts in parity rate. More sensitive to gradual drift
187 |         than simple threshold checks.
188 |         
189 |         Regulatory Basis:
190 |         - FFIEC: "Early warning indicators for operational risk"
191 |         - Basel III: "Timely identification of emerging risks"
192 |         
193 |         Args:
194 |             function_name: Payment function to analyze
195 |             tenant_id: Tenant profile for context
196 |             target_rate: Expected parity rate (default 95%)
197 |             threshold: CUSUM threshold for alarm (default 5.0)
198 |         
199 |         Returns:
200 |             Dictionary with CUSUM statistics and drift flag
201 |         """
202 |         history = self.get_history(function_name, tenant_id, limit=50)
203 |         
204 |         if len(history) < 5:
205 |             return {
206 |                 "drift_detected": False,
207 |                 "reason": "Insufficient history (need ≥5 runs)",
208 |                 "cusum_value": 0.0,
209 |                 "runs_analyzed": len(history)
210 |             }
211 |         
212 |         # Calculate CUSUM (cumulative deviations from target)
213 |         cusum = 0.0
214 |         max_cusum = 0.0
215 |         
216 |         for record in reversed(history):  # Oldest to newest
217 |             deviation = target_rate - record.parity_rate_pct
218 |             cusum = max(0, cusum + deviation)  # One-sided CUSUM (detect degradation)
219 |             max_cusum = max(max_cusum, cusum)
220 |         
221 |         drift_detected = cusum > threshold
222 |         
223 |         return {
224 |             "drift_detected": drift_detected,
225 |             "cusum_value": cusum,
226 |             "max_cusum": max_cusum,
227 |             "threshold": threshold,
228 |             "runs_analyzed": len(history),
229 |             "current_rate": history[0].parity_rate_pct if history else 0.0,
230 |             "target_rate": target_rate,
231 |             "severity": "HIGH" if cusum > threshold * 2 else "MEDIUM" if drift_detected else "LOW"
232 |         }
233 |     
234 |     def ewma_detect(self, function_name: str, tenant_id: str, 
235 |                     lambda_param: float = 0.2, control_limit: float = 3.0) -> Dict:
236 |         """
237 |         EWMA (Exponentially Weighted Moving Average) drift detection.
238 |         
239 |         Gives more weight to recent observations while considering history.
240 |         Good for detecting both gradual and sudden shifts.
241 |         
242 |         Regulatory Basis:
243 |         - Basel III: "Weighted historical data for risk assessment"
244 |         - FFIEC: "Trend analysis for operational metrics"
245 |         
246 |         Args:
247 |             function_name: Payment function to analyze
248 |             tenant_id: Tenant profile for context
249 |             lambda_param: Smoothing parameter (0-1, default 0.2)
250 |             control_limit: Number of standard deviations for alarm (default 3.0)
251 |         
252 |         Returns:
253 |             Dictionary with EWMA statistics and drift flag
254 |         """
255 |         history = self.get_history(function_name, tenant_id, limit=50)
256 |         
257 |         if len(history) < 5:
258 |             return {
259 |                 "drift_detected": False,
260 |                 "reason": "Insufficient history (need ≥5 runs)",
261 |                 "ewma_value": 0.0,
262 |                 "runs_analyzed": len(history)
263 |             }
264 |         
265 |         # Calculate EWMA
266 |         rates = [r.parity_rate_pct for r in reversed(history)]
267 |         ewma = rates[0]  # Initialize with first observation
268 |         
269 |         for rate in rates[1:]:
270 |             ewma = lambda_param * rate + (1 - lambda_param) * ewma
271 |         
272 |         # Calculate control limits
273 |         import numpy as np
274 |         mean_rate = np.mean(rates)
275 |         std_rate = np.std(rates)
276 |         
277 |         # EWMA standard deviation
278 |         ewma_std = std_rate * np.sqrt(lambda_param / (2 - lambda_param))
279 |         
280 |         lower_limit = mean_rate - control_limit * ewma_std
281 |         upper_limit = mean_rate + control_limit * ewma_std
282 |         
283 |         drift_detected = ewma < lower_limit or ewma > upper_limit
284 |         
285 |         return {
286 |             "drift_detected": drift_detected,
287 |             "ewma_value": ewma,
288 |             "mean_rate": mean_rate,
289 |             "std_rate": std_rate,
290 |             "lower_limit": lower_limit,
291 |             "upper_limit": upper_limit,
292 |             "control_limit_sigma": control_limit,
293 |             "runs_analyzed": len(history),
294 |             "current_rate": history[0].parity_rate_pct if history else 0.0,
295 |             "severity": "HIGH" if abs(ewma - mean_rate) > 2 * control_limit * ewma_std else "MEDIUM" if drift_detected else "LOW"
296 |         }
297 |     
298 |     def get_drift_summary(self, function_name: str, tenant_id: str) -> Dict:
299 |         """
300 |         Get comprehensive drift analysis combining multiple methods.
301 |         
302 |         Args:
303 |             function_name: Payment function to analyze
304 |             tenant_id: Tenant profile for context
305 |         
306 |         Returns:
307 |             Dictionary with all drift detection results and consensus
308 |         """
309 |         cusum = self.cusum_detect(function_name, tenant_id)
310 |         ewma = self.ewma_detect(function_name, tenant_id)
311 |         history = self.get_history(function_name, tenant_id, limit=10)
312 |         
313 |         # Consensus: drift if either method detects it
314 |         drift_detected = cusum.get("drift_detected", False) or ewma.get("drift_detected", False)
315 |         
316 |         # Calculate trend (improving/degrading/stable)
317 |         if len(history) >= 3:
318 |             recent_rates = [h.parity_rate_pct for h in history[:3]]
319 |             older_rates = [h.parity_rate_pct for h in history[3:6]] if len(history) >= 6 else recent_rates
320 |             
321 |             recent_avg = sum(recent_rates) / len(recent_rates)
322 |             older_avg = sum(older_rates) / len(older_rates)
323 |             
324 |             if recent_avg < older_avg - 2.0:
325 |                 trend = "DEGRADING"
326 |             elif recent_avg > older_avg + 2.0:
327 |                 trend = "IMPROVING"
328 |             else:
329 |                 trend = "STABLE"
330 |         else:
331 |             trend = "INSUFFICIENT_DATA"
332 |         
333 |         return {
334 |             "function_name": function_name,
335 |             "tenant_id": tenant_id,
336 |             "drift_detected": drift_detected,
337 |             "trend": trend,
338 |             "cusum": cusum,
339 |             "ewma": ewma,
340 |             "recent_history": [h.to_dict() for h in history[:5]],
341 |             "total_runs": len(history),
342 |             "recommendation": self._get_recommendation(drift_detected, trend, cusum, ewma)
343 |         }
344 |     
345 |     def _get_recommendation(self, drift_detected: bool, trend: str, 
346 |                            cusum: Dict, ewma: Dict) -> str:
347 |         """Generate actionable recommendation based on drift analysis."""
348 |         if not drift_detected:
349 |             return "No drift detected. Continue monitoring."
350 |         
351 |         if trend == "DEGRADING":
352 |             severity = max(
353 |                 ["LOW", "MEDIUM", "HIGH"].index(cusum.get("severity", "LOW")),
354 |                 ["LOW", "MEDIUM", "HIGH"].index(ewma.get("severity", "LOW"))
355 |             )
356 |             severity_label = ["LOW", "MEDIUM", "HIGH"][severity]
357 |             
358 |             if severity_label == "HIGH":
359 |                 return "URGENT: Significant parity degradation detected. Investigate immediately and consider blocking cutover."
360 |             elif severity_label == "MEDIUM":
361 |                 return "WARNING: Parity trending downward. Increase monitoring frequency and investigate root cause."
362 |             else:
363 |                 return "CAUTION: Minor parity variation detected. Monitor next few runs closely."
364 |         
365 |         return "Drift detected but trend unclear. Continue monitoring and gather more data."
366 | 
367 | # Made with Bob
</content>
</file>
<file><path>parity/compliance.py</path>
<content lines="1-465">
  1 | """
  2 | Regulatory compliance framework for banking migration cutover decisions.
  3 | 
  4 | Maps parity analysis results to specific regulatory requirements:
  5 | - FFIEC IT Handbook (Federal Financial Institutions Examination Council)
  6 | - Basel III Operational Risk Framework
  7 | - PSD2 (Payment Services Directive 2) - EU
  8 | - SWIFT gpi (Global Payments Innovation)
  9 | - SOX Section 404 (Sarbanes-Oxley)
 10 | 
 11 | Provides compliance scoring and attestation generation for audit trails.
 12 | """
 13 | 
 14 | from dataclasses import dataclass
 15 | from typing import List, Dict, Optional
 16 | from enum import Enum
 17 | 
 18 | 
 19 | class RegulatoryFramework(Enum):
 20 |     """Supported regulatory frameworks."""
 21 |     FFIEC = "FFIEC IT Handbook"
 22 |     BASEL_III = "Basel III Operational Risk"
 23 |     PSD2 = "Payment Services Directive 2"
 24 |     SWIFT_GPI = "SWIFT gpi Standards"
 25 |     SOX_404 = "Sarbanes-Oxley Section 404"
 26 |     GLBA = "Gramm-Leach-Bliley Act"
 27 | 
 28 | 
 29 | @dataclass
 30 | class ComplianceRequirement:
 31 |     """Single regulatory requirement with assessment criteria."""
 32 |     framework: RegulatoryFramework
 33 |     requirement_id: str
 34 |     title: str
 35 |     description: str
 36 |     assessment_criteria: str
 37 |     severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
 38 |     
 39 |     def to_dict(self) -> dict:
 40 |         return {
 41 |             "framework": self.framework.value,
 42 |             "requirement_id": self.requirement_id,
 43 |             "title": self.title,
 44 |             "description": self.description,
 45 |             "assessment_criteria": self.assessment_criteria,
 46 |             "severity": self.severity
 47 |         }
 48 | 
 49 | 
 50 | @dataclass
 51 | class ComplianceAssessment:
 52 |     """Assessment result for a single requirement."""
 53 |     requirement: ComplianceRequirement
 54 |     status: str  # "PASS", "FAIL", "PARTIAL", "NOT_APPLICABLE"
 55 |     evidence: str
 56 |     score: float  # 0-100
 57 |     recommendations: List[str]
 58 |     
 59 |     def to_dict(self) -> dict:
 60 |         return {
 61 |             "requirement": self.requirement.to_dict(),
 62 |             "status": self.status,
 63 |             "evidence": self.evidence,
 64 |             "score": self.score,
 65 |             "recommendations": self.recommendations
 66 |         }
 67 | 
 68 | 
 69 | class ComplianceFramework:
 70 |     """
 71 |     Regulatory compliance assessment for migration cutover decisions.
 72 |     
 73 |     Maps parity analysis results to regulatory requirements and generates
 74 |     compliance scores with audit-ready attestations.
 75 |     """
 76 |     
 77 |     def __init__(self):
 78 |         """Initialize compliance framework with regulatory requirements."""
 79 |         self.requirements = self._load_requirements()
 80 |     
 81 |     def _load_requirements(self) -> List[ComplianceRequirement]:
 82 |         """Load all regulatory requirements."""
 83 |         return [
 84 |             # FFIEC Requirements
 85 |             ComplianceRequirement(
 86 |                 framework=RegulatoryFramework.FFIEC,
 87 |                 requirement_id="FFIEC-IT-001",
 88 |                 title="Risk-Based Testing Approach",
 89 |                 description="Testing should be commensurate with the size, complexity, and risk profile of the institution",
 90 |                 assessment_criteria="Parity threshold matches institution tier (Tier 1: 99%, Tier 2: 95%, Community: 90%)",
 91 |                 severity="CRITICAL"
 92 |             ),
 93 |             ComplianceRequirement(
 94 |                 framework=RegulatoryFramework.FFIEC,
 95 |                 requirement_id="FFIEC-IT-002",
 96 |                 title="Operational Risk Monitoring",
 97 |                 description="Continuous monitoring of operational risk indicators with timely escalation",
 98 |                 assessment_criteria="Drift detection active with CUSUM/EWMA monitoring and alerting",
 99 |                 severity="HIGH"
100 |             ),
101 |             ComplianceRequirement(
102 |                 framework=RegulatoryFramework.FFIEC,
103 |                 requirement_id="FFIEC-IT-003",
104 |                 title="Change Management Documentation",
105 |                 description="Comprehensive documentation of system changes with audit trail",
106 |                 assessment_criteria="PDF audit reports generated with timestamp, tenant profile, and verdicts",
107 |                 severity="HIGH"
108 |             ),
109 |             
110 |             # Basel III Requirements
111 |             ComplianceRequirement(
112 |                 framework=RegulatoryFramework.BASEL_III,
113 |                 requirement_id="BASEL-OR-001",
114 |                 title="Operational Risk Assessment",
115 |                 description="Institution-specific operational risk assessment based on internal data",
116 |                 assessment_criteria="Tenant-specific risk weights applied (12-15% based on institution tier)",
117 |                 severity="CRITICAL"
118 |             ),
119 |             ComplianceRequirement(
120 |                 framework=RegulatoryFramework.BASEL_III,
121 |                 requirement_id="BASEL-OR-002",
122 |                 title="Loss Event Tracking",
123 |                 description="Systematic collection and analysis of operational loss events",
124 |                 assessment_criteria="Anomaly detection with >2σ flagging and historical tracking",
125 |                 severity="HIGH"
126 |             ),
127 |             ComplianceRequirement(
128 |                 framework=RegulatoryFramework.BASEL_III,
129 |                 requirement_id="BASEL-OR-003",
130 |                 title="Model Validation",
131 |                 description="Independent validation of risk models with multiple methodologies",
132 |                 assessment_criteria="Multiple confidence interval methods (Wilson, Bootstrap, Bayesian) for validation",
133 |                 severity="MEDIUM"
134 |             ),
135 |             
136 |             # PSD2 Requirements (EU)
137 |             ComplianceRequirement(
138 |                 framework=RegulatoryFramework.PSD2,
139 |                 requirement_id="PSD2-ART45",
140 |                 title="FX Transparency",
141 |                 description="Clear disclosure of foreign exchange rates and margins",
142 |                 assessment_criteria="FX margin divergence detected and flagged (Legacy 2.0% vs Modern 0.05%)",
143 |                 severity="CRITICAL"
144 |             ),
145 |             ComplianceRequirement(
146 |                 framework=RegulatoryFramework.PSD2,
147 |                 requirement_id="PSD2-ART52",
148 |                 title="Payment Service Quality",
149 |                 description="Continuous monitoring of payment service availability and performance",
150 |                 assessment_criteria="Latency tracking and parity monitoring across all payment functions",
151 |                 severity="HIGH"
152 |             ),
153 |             
154 |             # SWIFT gpi Requirements
155 |             ComplianceRequirement(
156 |                 framework=RegulatoryFramework.SWIFT_GPI,
157 |                 requirement_id="SWIFT-GPI-001",
158 |                 title="Fee Transparency",
159 |                 description="Clear and consistent fee disclosure for cross-border payments",
160 |                 assessment_criteria="Fee divergence detected and quantified (Legacy vs Modern pricing)",
161 |                 severity="HIGH"
162 |             ),
163 |             ComplianceRequirement(
164 |                 framework=RegulatoryFramework.SWIFT_GPI,
165 |                 requirement_id="SWIFT-GPI-002",
166 |                 title="Payment Tracking",
167 |                 description="End-to-end payment tracking with status updates",
168 |                 assessment_criteria="Transaction pair tracking with legacy/modern comparison",
169 |                 severity="MEDIUM"
170 |             ),
171 |             
172 |             # SOX 404 Requirements
173 |             ComplianceRequirement(
174 |                 framework=RegulatoryFramework.SOX_404,
175 |                 requirement_id="SOX-404-001",
176 |                 title="Internal Controls Assessment",
177 |                 description="Management assessment of internal controls over financial reporting",
178 |                 assessment_criteria="Automated parity checks with documented thresholds and verdicts",
179 |                 severity="CRITICAL"
180 |             ),
181 |             ComplianceRequirement(
182 |                 framework=RegulatoryFramework.SOX_404,
183 |                 requirement_id="SOX-404-002",
184 |                 title="Control Testing Documentation",
185 |                 description="Evidence of control testing with results and remediation",
186 |                 assessment_criteria="PDF audit reports with function-level verdicts and exposure calculations",
187 |                 severity="HIGH"
188 |             ),
189 |         ]
190 |     
191 |     def assess_compliance(self, scores: List[dict], tenant_profile: dict, 
192 |                          drift_summary: Optional[Dict] = None) -> List[ComplianceAssessment]:
193 |         """
194 |         Assess compliance across all regulatory requirements.
195 |         
196 |         Args:
197 |             scores: Function scores from parity analysis
198 |             tenant_profile: Tenant configuration used
199 |             drift_summary: Optional drift detection results
200 |         
201 |         Returns:
202 |             List of ComplianceAssessment objects
203 |         """
204 |         assessments = []
205 |         
206 |         for req in self.requirements:
207 |             assessment = self._assess_requirement(req, scores, tenant_profile, drift_summary)
208 |             assessments.append(assessment)
209 |         
210 |         return assessments
211 |     
212 |     def _assess_requirement(self, req: ComplianceRequirement, scores: List[dict],
213 |                            tenant_profile: dict, drift_summary: Optional[Dict]) -> ComplianceAssessment:
214 |         """Assess a single regulatory requirement."""
215 |         
216 |         # FFIEC-IT-001: Risk-Based Testing
217 |         if req.requirement_id == "FFIEC-IT-001":
218 |             threshold = tenant_profile.get("parity_threshold_pct", 95)
219 |             tier = tenant_profile.get("tier", "tier2")
220 |             
221 |             expected_thresholds = {"tier1": 99, "tier2": 95, "community": 90}
222 |             expected = expected_thresholds.get(tier, 95)
223 |             
224 |             if threshold == expected:
225 |                 return ComplianceAssessment(
226 |                     requirement=req,
227 |                     status="PASS",
228 |                     evidence=f"Parity threshold ({threshold}%) matches {tier} institution requirements",
229 |                     score=100.0,
230 |                     recommendations=[]
231 |                 )
232 |             else:
233 |                 return ComplianceAssessment(
234 |                     requirement=req,
235 |                     status="PARTIAL",
236 |                     evidence=f"Parity threshold ({threshold}%) differs from expected {tier} threshold ({expected}%)",
237 |                     score=70.0,
238 |                     recommendations=[f"Consider adjusting threshold to {expected}% for {tier} institutions"]
239 |                 )
240 |         
241 |         # FFIEC-IT-002: Operational Risk Monitoring
242 |         elif req.requirement_id == "FFIEC-IT-002":
243 |             if drift_summary:
244 |                 drift_detected = drift_summary.get("drift_detected", False)
245 |                 if not drift_detected:
246 |                     return ComplianceAssessment(
247 |                         requirement=req,
248 |                         status="PASS",
249 |                         evidence="Drift detection active with CUSUM and EWMA monitoring. No drift detected.",
250 |                         score=100.0,
251 |                         recommendations=[]
252 |                     )
253 |                 else:
254 |                     trend = drift_summary.get("trend", "UNKNOWN")
255 |                     return ComplianceAssessment(
256 |                         requirement=req,
257 |                         status="FAIL",
258 |                         evidence=f"Drift detected: {trend} trend. CUSUM/EWMA monitoring active.",
259 |                         score=40.0,
260 |                         recommendations=[drift_summary.get("recommendation", "Investigate drift cause")]
261 |                     )
262 |             else:
263 |                 return ComplianceAssessment(
264 |                     requirement=req,
265 |                     status="PARTIAL",
266 |                     evidence="Drift detection capability available but not executed for this run",
267 |                     score=60.0,
268 |                     recommendations=["Enable drift detection for continuous monitoring"]
269 |                 )
270 |         
271 |         # FFIEC-IT-003: Change Management Documentation
272 |         elif req.requirement_id == "FFIEC-IT-003":
273 |             return ComplianceAssessment(
274 |                 requirement=req,
275 |                 status="PASS",
276 |                 evidence="PDF audit report generated with timestamp, tenant profile, function verdicts, and exposure",
277 |                 score=100.0,
278 |                 recommendations=[]
279 |             )
280 |         
281 |         # BASEL-OR-001: Operational Risk Assessment
282 |         elif req.requirement_id == "BASEL-OR-001":
283 |             risk_weight = tenant_profile.get("basel_operational_risk_weight", 15)
284 |             tier = tenant_profile.get("tier", "tier2")
285 |             
286 |             if (tier == "tier1" and risk_weight == 12) or (tier in ["tier2", "community"] and risk_weight == 15):
287 |                 return ComplianceAssessment(
288 |                     requirement=req,
289 |                     status="PASS",
290 |                     evidence=f"Basel III risk weight ({risk_weight}%) appropriate for {tier} institution",
291 |                     score=100.0,
292 |                     recommendations=[]
293 |                 )
294 |             else:
295 |                 return ComplianceAssessment(
296 |                     requirement=req,
297 |                     status="PARTIAL",
298 |                     evidence=f"Risk weight ({risk_weight}%) may not align with {tier} institution profile",
299 |                     score=75.0,
300 |                     recommendations=["Review Basel III risk weight calibration"]
301 |                 )
302 |         
303 |         # BASEL-OR-002: Loss Event Tracking
304 |         elif req.requirement_id == "BASEL-OR-002":
305 |             total_anomalies = sum(s.get("anomaly_count", 0) for s in scores)
306 |             sigma_threshold = tenant_profile.get("anomaly_sigma_threshold", 2.0)
307 |             
308 |             return ComplianceAssessment(
309 |                 requirement=req,
310 |                 status="PASS",
311 |                 evidence=f"Anomaly detection active with {sigma_threshold}σ threshold. {total_anomalies} anomalies detected.",
312 |                 score=100.0,
313 |                 recommendations=[] if total_anomalies == 0 else ["Investigate flagged anomalies"]
314 |             )
315 |         
316 |         # BASEL-OR-003: Model Validation
317 |         elif req.requirement_id == "BASEL-OR-003":
318 |             return ComplianceAssessment(
319 |                 requirement=req,
320 |                 status="PASS",
321 |                 evidence="Multiple confidence interval methods available (Wilson, Bootstrap, Bayesian) for model validation",
322 |                 score=100.0,
323 |                 recommendations=["Consider running all CI methods for critical functions"]
324 |             )
325 |         
326 |         # PSD2-ART45: FX Transparency
327 |         elif req.requirement_id == "PSD2-ART45":
328 |             psd2_jurisdiction = tenant_profile.get("psd2_jurisdiction", False)
329 |             
330 |             if not psd2_jurisdiction:
331 |                 return ComplianceAssessment(
332 |                     requirement=req,
333 |                     status="NOT_APPLICABLE",
334 |                     evidence="Institution not in PSD2 jurisdiction",
335 |                     score=100.0,
336 |                     recommendations=[]
337 |                 )
338 |             
339 |             # Check for FX-related functions
340 |             intl_wire = next((s for s in scores if "International" in s["function"]), None)
341 |             if intl_wire and intl_wire["verdict"] == "DO_NOT_CUT":
342 |                 return ComplianceAssessment(
343 |                     requirement=req,
344 |                     status="PASS",
345 |                     evidence=f"FX margin divergence detected and blocked: {intl_wire['function']}",
346 |                     score=100.0,
347 |                     recommendations=["Resolve FX margin discrepancy before cutover"]
348 |                 )
349 |             else:
350 |                 return ComplianceAssessment(
351 |                     requirement=req,
352 |                     status="PASS",
353 |                     evidence="No FX margin issues detected in current analysis",
354 |                     score=100.0,
355 |                     recommendations=[]
356 |                 )
357 |         
358 |         # Default assessment for other requirements
359 |         else:
360 |             return ComplianceAssessment(
361 |                 requirement=req,
362 |                 status="PASS",
363 |                 evidence="Requirement assessed as compliant based on system capabilities",
364 |                 score=90.0,
365 |                 recommendations=[]
366 |             )
367 |     
368 |     def get_compliance_score(self, assessments: List[ComplianceAssessment]) -> Dict:
369 |         """
370 |         Calculate overall compliance score across all frameworks.
371 |         
372 |         Args:
373 |             assessments: List of compliance assessments
374 |         
375 |         Returns:
376 |             Dictionary with overall and per-framework scores
377 |         """
378 |         if not assessments:
379 |             return {"overall_score": 0.0, "framework_scores": {}}
380 |         
381 |         # Overall score (weighted by severity)
382 |         severity_weights = {"CRITICAL": 3.0, "HIGH": 2.0, "MEDIUM": 1.5, "LOW": 1.0}
383 |         
384 |         total_weighted_score = 0.0
385 |         total_weight = 0.0
386 |         
387 |         for assessment in assessments:
388 |             weight = severity_weights.get(assessment.requirement.severity, 1.0)
389 |             total_weighted_score += assessment.score * weight
390 |             total_weight += weight
391 |         
392 |         overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
393 |         
394 |         # Per-framework scores
395 |         framework_scores = {}
396 |         for framework in RegulatoryFramework:
397 |             framework_assessments = [a for a in assessments if a.requirement.framework == framework]
398 |             if framework_assessments:
399 |                 avg_score = sum(a.score for a in framework_assessments) / len(framework_assessments)
400 |                 framework_scores[framework.value] = {
401 |                     "score": avg_score,
402 |                     "total_requirements": len(framework_assessments),
403 |                     "passed": sum(1 for a in framework_assessments if a.status == "PASS"),
404 |                     "failed": sum(1 for a in framework_assessments if a.status == "FAIL")
405 |                 }
406 |         
407 |         return {
408 |             "overall_score": overall_score,
409 |             "framework_scores": framework_scores,
410 |             "total_requirements": len(assessments),
411 |             "critical_failures": sum(1 for a in assessments if a.status == "FAIL" and a.requirement.severity == "CRITICAL")
412 |         }
413 |     
414 |     def generate_attestation(self, assessments: List[ComplianceAssessment], 
415 |                             compliance_score: Dict, tenant_profile: dict) -> str:
416 |         """
417 |         Generate regulatory attestation document.
418 |         
419 |         Args:
420 |             assessments: List of compliance assessments
421 |             compliance_score: Overall compliance score
422 |             tenant_profile: Tenant configuration
423 |         
424 |         Returns:
425 |             Formatted attestation text for audit reports
426 |         """
427 |         from datetime import datetime, timezone
428 |         
429 |         timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
430 |         
431 |         attestation = f"""
432 | REGULATORY COMPLIANCE ATTESTATION
433 | Generated: {timestamp}
434 | Institution: {tenant_profile.get('name', 'Unknown')}
435 | Tenant ID: {tenant_profile.get('tenant_id', 'Unknown')}
436 | 
437 | OVERALL COMPLIANCE SCORE: {compliance_score['overall_score']:.1f}/100
438 | 
439 | FRAMEWORK COMPLIANCE:
440 | """
441 |         
442 |         for framework, data in compliance_score['framework_scores'].items():
443 |             attestation += f"\n{framework}:\n"
444 |             attestation += f"  Score: {data['score']:.1f}/100\n"
445 |             attestation += f"  Requirements: {data['passed']}/{data['total_requirements']} passed\n"
446 |         
447 |         attestation += f"\n\nCRITICAL FAILURES: {compliance_score['critical_failures']}\n"
448 |         
449 |         if compliance_score['critical_failures'] > 0:
450 |             attestation += "\nWARNING: Critical compliance failures detected. Cutover NOT RECOMMENDED.\n"
451 |             attestation += "\nFailed Requirements:\n"
452 |             for assessment in assessments:
453 |                 if assessment.status == "FAIL" and assessment.requirement.severity == "CRITICAL":
454 |                     attestation += f"  - {assessment.requirement.requirement_id}: {assessment.requirement.title}\n"
455 |                     attestation += f"    Evidence: {assessment.evidence}\n"
456 |         else:
457 |             attestation += "\nAll critical requirements satisfied. Cutover may proceed subject to risk assessment.\n"
458 |         
459 |         attestation += "\n" + "="*80 + "\n"
460 |         attestation += "This attestation is generated automatically by Bob the Judge.\n"
461 |         attestation += "Manual review and sign-off required before production cutover.\n"
462 |         
463 |         return attestation
464 | 
465 | # Made with Bob
</content>
</file>
<file><path>dashboard.py</path><file_outline>File: dashboard.py (1070 lines)

Function: _check_service (lines 173-179)
  Variable: url (lines 173-173)
  Variable: timeout (lines 173-173)
  Variable: r (lines 176-176)
Function: _check_mcp_running (lines 181-190)
  Variable: r (lines 184-184)
Variable: legacy_up (lines 192-192)
Variable: modern_up (lines 193-193)
Variable: bob_live (lines 194-194)
Variable: mcp_active (lines 195-195)
Variable: services (lines 210-210)
Variable: name (lines 216-216)
Variable: port (lines 216-216)
Variable: ok (lines 216-216)
Variable: dot (lines 218-218)
Variable: status_label (lines 219-219)
Variable: available_tenants (lines 238-238)
Variable: tenant_options (lines 239-239)
Variable: selected_tenant_id (lines 246-246)
Variable: tenant (lines 258-258)
Variable: n_runs (lines 270-270)
Variable: last_run (lines 271-271)
Variable: last_run_str (lines 272-272)
Variable: arch_steps (lines 281-281)
Variable: step (lines 289-289)
Variable: now_str (lines 303-303)
Variable: bob_label (lines 304-304)
Variable: bob_color (lines 305-305)
Variable: mcp_label (lines 306-306)
Variable: mcp_color (lines 307-307)
Variable: ctrl1 (lines 381-381)
Variable: ctrl2 (lines 381-381)
Variable: ctrl3 (lines 381-381)
Variable: ctrl4 (lines 381-381)
Variable: ctrl5 (lines 381-381)
Variable: n_transactions (lines 383-383)
Variable: run_analysis (lines 386-386)
Variable: export_pdf (lines 389-389)
Variable: live_mode (lines 392-392)
Variable: demo_mode (lines 395-395)
Variable: _scan_ph (lines 399-399)
Function: _show_scan (lines 401-410)
  Variable: pct (lines 401-401)
  Variable: msg (lines 401-401)
Variable: pairs (lines 416-416)
Variable: _conn_err (lines 417-417)
Variable: tenant_id (lines 428-428)
Variable: results (lines 432-432)
Variable: scores (lines 435-435)
Variable: entry (lines 444-444)
Variable: s (lines 445-445)
Variable: run_ts (lines 451-451)
Variable: bob_resp (lines 455-455)
Variable: bob_sid (lines 456-456)
Variable: current_tenant (lines 459-459)
Variable: tenant_profile (lines 460-460)
Variable: pdf_bytes (lines 463-463)
Variable: filename (lines 464-464)
Variable: total_txns (lines 484-484)
Variable: overall_parity (lines 485-485)
Variable: safe_functions (lines 486-486)
Variable: do_not_cut (lines 487-487)
Variable: total_exposure (lines 488-488)
Variable: anomaly_count (lines 492-492)
Variable: db_color (lines 496-496)
Variable: db_bg (lines 496-496)
Variable: db_icon (lines 497-497)
Variable: db_main (lines 497-497)
Variable: db_sub (lines 498-498)
Variable: k1 (lines 531-531)
Variable: k2 (lines 531-531)
Variable: k3 (lines 531-531)
Variable: k4 (lines 531-531)
Variable: k5 (lines 531-531)
Variable: k6 (lines 531-531)
Variable: colour (lines 539-539)
Variable: c (lines 552-552)
Variable: exp_colour (lines 559-559)
Variable: exp_str (lines 560-560)
Variable: an_colour (lines 567-567)
Constant: CARBON_VERDICT (lines 577-577)
Variable: cols (lines 584-584)
Variable: col (lines 585-585)
Variable: v (lines 586-586)
Variable: ci_lo (lines 587-587)
Variable: ci_hi (lines 588-588)
Variable: exp (lines 589-589)
Variable: patch_active (lines 614-614)
Variable: show_patch_section (lines 615-615)
Variable: pcol1 (lines 630-630)
Variable: pcol2 (lines 630-630)
Variable: apply_patch_btn (lines 632-632)
Variable: bob_patch (lines 645-645)
Variable: e (lines 655-655)
Variable: pairs_new (lines 659-659)
Variable: results_new (lines 660-660)
Variable: scores_new (lines 662-662)
Variable: rcol1 (lines 690-690)
Variable: rcol2 (lines 690-690)
Variable: reset_btn (lines 692-692)
Variable: resp (lines 719-719)
Constant: IBM_CHART_THEME (lines 744-744)
Variable: history (lines 752-752)
Variable: has_history (lines 753-753)
Variable: tab_labels (lines 754-754)
Variable: tabs (lines 755-755)
Variable: df (lines 759-759)
Variable: fig (lines 760-760)
Variable: color_map (lines 761-761)
Variable: row (lines 762-762)
Variable: bar_color (lines 763-763)
Variable: df_r (lines 784-784)
Variable: fig2 (lines 785-785)
Variable: _radar_labels (lines 799-799)
Variable: _radar_labels_closed (lines 800-800)
Variable: _radar_vals (lines 801-801)
Variable: _radar_vals_closed (lines 802-802)
Variable: _threshold_closed (lines 803-803)
Variable: _color_map (lines 804-804)
Variable: _dominant_verdict (lines 805-805)
Variable: _fill_color (lines 806-806)
Variable: _fill_rgba (lines 807-807)
Variable: r (lines 808-808)
Variable: g (lines 808-808)
Variable: b (lines 808-808)
Variable: fig_radar (lines 809-809)
Variable: df_hist (lines 841-841)
Variable: fn_colors (lines 842-842)
Variable: fig_hist (lines 848-848)
Variable: fn (lines 849-849)
Variable: color (lines 850-850)
Variable: divergent (lines 868-868)
Variable: worst (lines 872-872)
Variable: sev_colors (lines 877-877)
Variable: diff_cols (lines 878-878)
Variable: i (lines 880-880)
Variable: tx_label (lines 883-883)
Variable: anomaly_badge (lines 884-884)
Variable: sigma (lines 886-886)
Variable: d (lines 895-895)
Variable: sev_c (lines 896-896)
Variable: field_label (lines 897-897)
Variable: legacy_val (lines 898-898)
Variable: modern_val (lines 899-899)
Variable: diff_val (lines 900-900)
Variable: reg (lines 901-901)
Variable: lc (lines 903-903)
Variable: mc (lines 903-903)
Variable: rows (lines 935-935)
Variable: df_div (lines 950-950)
Function: colour_sev (lines 952-953)
  Variable: val (lines 952-952)
Variable: safe (lines 967-967)
Variable: monitor (lines 968-968)
Variable: hold (lines 969-969)
Variable: rec1 (lines 971-971)
Variable: rec2 (lines 971-971)
Variable: rec3 (lines 971-971)
Variable: items (lines 973-973)
Variable: bob_col1 (lines 997-997)
Variable: bob_col2 (lines 997-997)
Variable: bob_mode (lines 1000-1000)
Variable: ask_bob_btn (lines 1010-1010)
Variable: mode_prompts (lines 1013-1013)
Variable: bob_context (lines 1019-1019)
Variable: response (lines 1028-1028)
Variable: is_live (lines 1033-1033)
Variable: tag_class (lines 1034-1034)
Variable: tag_text (lines 1035-1035)
Variable: countdown_ph (lines 1047-1047)
Variable: remaining (lines 1048-1048)
</file_outline>
<notice>This file is large (1069 lines). You will use the following strategy to understand this file:
- Inform the user you are going to use large file strategy, to efficiently understand the file
- Use the file_outline provided to get an overview of the file structure to help decide next action. This is not the full file. It is not the full depth of the contents.
- If you read the file, use precise file reads with line ranges for specific sections of interest
- Consider if other commands/tools are better suited for extracting information from that file type
- Use ask_followup_question tool if needed to identify the best next action
</notice></file>
</files>
Tool [read_file] was not executed because a tool has already been used in this message. Only one tool may be used per message. You must assess the first tool's result before proceeding to use the next tool.
Tool [read_file] was not executed because a tool has already been used in this message. Only one tool may be used per message. You must assess the first tool's result before proceeding to use the next tool.
<environment_details>
# VSCode Visible Files
dashboard.py

# VSCode Open Tabs
parity/tenant_config.py,config/tenants.json,parity/parity_engine.py,parity/scoring.py,dashboard.py,parity/confidence.py,parity/drift_detection.py,parity/compliance.py,mcp_server.py,audit/pdf_report.py,ENHANCEMENT_GUIDE.md,tests/test_tenant_config.py,tests/test_confidence.py,tests/test_drift_detection.py,tests/__init__.py,requirements.txt,tests/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-15T18:04:31.189Z
User time zone: Europe/Berlin, UTC+2:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll conduct a comprehensive code review of the specified files. Let me read the remaining files to complete my analysis.

<read_file>
<args>
  <file>
    <path>mcp_server.py</path>
  </file>
  <file>
    <path>audit/pdf_report.py</path>
  </file>
  <file>
    <path>dashboard.py</path>
    <line_range>1-200</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'mcp_server.py', 'audit/pdf_report.py', 'dashboard.py'] Result:
<files>
<file><path>mcp_server.py</path>
<content lines="1-596">
  1 | """
  2 | Bob the Judge — MCP Server
  3 | Exposes cutover analysis tools so IBM Bob can call them in Orchestrator mode.
  4 | 
  5 | Configure in Bob IDE (.bob/mcp.json):
  6 | {
  7 |   "mcpServers": {
  8 |     "bob-the-judge": {
  9 |       "command": "python",
 10 |       "args": ["mcp_server.py"],
 11 |       "cwd": "<path-to-bob-the-judge>"
 12 |     }
 13 |   }
 14 | }
 15 | 
 16 | Then in Bob Orchestrator mode, Bob can:
 17 |   - Run live parity analysis
 18 |   - Query per-function verdicts
 19 |   - Get dollar exposure summary
 20 |   - Check anomaly flags
 21 | """
 22 | 
 23 | import asyncio
 24 | import json
 25 | from mcp.server.fastmcp import FastMCP
 26 | 
 27 | mcp = FastMCP(
 28 |     "bob-the-judge",
 29 |     instructions=(
 30 |         "You are connected to Bob the Judge — a live migration cutover advisor. "
 31 |         "Use analyze_cutover_readiness to run a fresh analysis, get_function_verdict to check "
 32 |         "a specific payment function, and get_risk_summary for executive-level exposure figures."
 33 |     ),
 34 | )
 35 | 
 36 | 
 37 | # ── Tool: run live parity analysis ───────────────────────────────────────────
 38 | @mcp.tool()
 39 | async def analyze_cutover_readiness(n_transactions: int = 60, tenant_id: str = "demo_default") -> str:
 40 |     """
 41 |     Run live parity analysis across all payment functions with tenant-specific thresholds.
 42 |     Sends identical transactions to both legacy (COBOL) and modern systems,
 43 |     compares outputs, and returns cutover verdicts with confidence intervals.
 44 | 
 45 |     Args:
 46 |         n_transactions: Number of transactions to sample (20–200).
 47 |         tenant_id: Tenant profile ID (tier1_global, tier2_regional, community_bank, demo_default).
 48 |     """
 49 |     from parity.traffic_generator import run_batch
 50 |     from parity.parity_engine import analyse_batch, flag_anomalies
 51 |     from parity.scoring import score_results
 52 |     from parity.tenant_config import load_tenant
 53 | 
 54 |     tenant = load_tenant(tenant_id)
 55 |     pairs = await run_batch(n=max(20, min(n_transactions, 200)))
 56 |     results = analyse_batch(pairs, tenant=tenant)
 57 |     results = flag_anomalies(results, tenant=tenant)
 58 |     scores = score_results(results, tenant=tenant)
 59 | 
 60 |     anomalies = sum(1 for r in results if r.get("anomaly"))
 61 |     total_exposure = sum(
 62 |         s.get("exposure_usd", 0) for s in scores
 63 |         if s["verdict"] in ("DO_NOT_CUT", "HOLD_INVESTIGATE")
 64 |     )
 65 | 
 66 |     lines = [
 67 |         "BOB THE JUDGE — CUTOVER READINESS REPORT",
 68 |         "=" * 44,
 69 |         f"Tenant Profile        : {tenant_id} ({tenant.ffiec_category})",
 70 |         f"Parity Threshold      : {tenant.parity_threshold_pct}%",
 71 |         f"Fee Tolerance         : ${tenant.fee_tolerance_usd:.2f}",
 72 |         f"Anomaly Sigma         : {tenant.anomaly_sigma_threshold}σ",
 73 |         "",
 74 |         f"Transactions analysed : {len(results)}",
 75 |         f"Anomalies detected    : {anomalies}",
 76 |         f"Total $ exposure      : ${total_exposure:,.0f}",
 77 |         "",
 78 |     ]
 79 | 
 80 |     for s in scores:
 81 |         ci = f"{s['ci_low']:.1f}%–{s['ci_high']:.1f}%"
 82 |         lines += [
 83 |             f"[ {s['verdict']} ]  {s['function']}",
 84 |             f"  Readiness : {s['readiness_score']:.0f}/100",
 85 |             f"  Parity    : {s['parity_rate_pct']:.1f}%  (95% CI {ci}  n={s['total_transactions']})",
 86 |             f"  Exposure  : ${s.get('exposure_usd', 0):,.0f}",
 87 |             f"  Fee delta : ${s['avg_fee_diff_usd']:.4f} avg",
 88 |             "",
 89 |         ]
 90 | 
 91 |     return "\n".join(lines)
 92 | 
 93 | 
 94 | # ── Tool: single function verdict ─────────────────────────────────────────────
 95 | @mcp.tool()
 96 | def get_function_verdict(function_name: str) -> str:
 97 |     """
 98 |     Get the cutover verdict and key metrics for a specific payment function.
 99 | 
100 |     Args:
101 |         function_name: One of 'Domestic Wire Transfer', 'International Wire Transfer',
102 |                        'Scheduled Payment', 'High-Value Wire Transfer'.
103 |     """
104 |     verdicts = {
105 |         "Domestic Wire Transfer": {
106 |             "verdict": "SAFE_TO_CUT",
107 |             "parity": "100%",
108 |             "reason": "Fee rounding within $0.02 tolerance. ROUND_HALF_DOWN vs ROUND_HALF_UP difference is negligible at domestic amounts.",
109 |             "action": "Proceed with cutover. No regulatory risk.",
110 |         },
111 |         "Scheduled Payment": {
112 |             "verdict": "SAFE_TO_CUT",
113 |             "parity": "100%",
114 |             "reason": "Low-value fixed amounts produce identical outputs on both systems.",
115 |             "action": "Proceed with cutover.",
116 |         },
117 |         "International Wire Transfer": {
118 |             "verdict": "DO_NOT_CUT",
119 |             "parity": "0%",
120 |             "reason": "FX margin divergence: Legacy charges fixed 2.0% FX spread (decade-old contract). "
121 |                       "Modern uses real-time 0.05% spread. Delta reaches $794 on a $40K transaction.",
122 |             "action": "BLOCK cutover. Fix FX margin contract before proceeding. Regulation: PSD2 Art. 45.",
123 |         },
124 |         "High-Value Wire Transfer": {
125 |             "verdict": "DO_NOT_CUT",
126 |             "parity": "0%",
127 |             "reason": "Fee structure divergence: Legacy SWIFT pricing (0.15% + $15 flat) vs "
128 |                       "Modern pricing (0.08% + $10 flat). Delta reaches $158 on a $218K transfer.",
129 |             "action": "BLOCK cutover. Align fee schedules with compliance team. Regulation: SWIFT gpi SLA.",
130 |         },
131 |     }
132 | 
133 |     v = verdicts.get(function_name)
134 |     if not v:
135 |         available = ", ".join(verdicts.keys())
136 |         return f"Function '{function_name}' not found.\nAvailable functions: {available}"
137 | 
138 |     return (
139 |         f"FUNCTION: {function_name}\n"
140 |         f"VERDICT : {v['verdict']}\n"
141 |         f"PARITY  : {v['parity']}\n"
142 |         f"REASON  : {v['reason']}\n"
143 |         f"ACTION  : {v['action']}"
144 |     )
145 | 
146 | 
147 | # ── Tool: executive risk summary ──────────────────────────────────────────────
148 | @mcp.tool()
149 | def get_risk_summary() -> str:
150 |     """
151 |     Return an executive-level dollar exposure and risk summary for the CTO briefing.
152 |     Based on current parity analysis results.
153 |     """
154 |     return """EXECUTIVE RISK SUMMARY — Bob the Judge
155 | 
156 | SAFE TO CUT OVER NOW:
157 |   ✓ Domestic Wire Transfer   — 100% parity, zero exposure
158 |   ✓ Scheduled Payment        — 100% parity, zero exposure
159 | 
160 | BLOCKED — DO NOT CUT:
161 |   ✗ International Wire Transfer
162 |       Exposure     : $2.1M–$4.8M projected daily volume at risk
163 |       Root cause   : FX margin (2.0% legacy vs 0.05% modern)
164 |       Regulation   : PSD2 Art. 45 — FX Transparency
165 |       Fix estimate : 3–5 days (contract renegotiation + code patch)
166 | 
167 |   ✗ High-Value Wire Transfer
168 |       Exposure     : $890K–$2.3M projected daily volume at risk
169 |       Root cause   : Fee schedule mismatch (SWIFT legacy vs modern pricing)
170 |       Regulation   : SWIFT gpi SLA — Fee Consistency
171 |       Fix estimate : 1–2 days (fee table update)
172 | 
173 | RECOMMENDATION:
174 |   Cut over Domestic + Scheduled immediately.
175 |   Hold International + High-Value until fee/FX fixes verified.
176 |   Estimated days to full cutover: 5–7 working days.
177 | """
178 | 
179 | 
180 | # ── Tool: list monitored functions ────────────────────────────────────────────
181 | @mcp.tool()
182 | def list_monitored_functions() -> str:
183 |     """List all payment functions currently being monitored for cutover readiness."""
184 |     return """MONITORED PAYMENT FUNCTIONS
185 | 
186 | 1. Domestic Wire Transfer
187 |    Volume range : $10 – $9,999 USD
188 |    Legacy port  : 8001  |  Modern port: 8002
189 |    Status       : SAFE_TO_CUT
190 | 
191 | 2. International Wire Transfer
192 |    Volume range : $100 – $49,999 (multi-currency)
193 |    Legacy port  : 8001  |  Modern port: 8002
194 |    Status       : DO_NOT_CUT
195 | 
196 | 3. Scheduled Payment
197 |    Volume range : $1 – $499 USD
198 |    Legacy port  : 8001  |  Modern port: 8002
199 |    Status       : SAFE_TO_CUT
200 | 
201 | 4. High-Value Wire Transfer
202 |    Volume range : $5,000 – $500,000 USD
203 |    Legacy port  : 8001  |  Modern port: 8002
204 |    Status       : DO_NOT_CUT
205 | """
206 | 
207 | 
208 | # ── Tool: list tenant profiles ────────────────────────────────────────────────
209 | @mcp.tool()
210 | def list_tenant_profiles() -> str:
211 |     """
212 |     List all available tenant profiles with their risk-appropriate thresholds.
213 |     Each profile is calibrated for different bank tiers per FFIEC, Basel III, and PSD2.
214 |     """
215 |     from parity.tenant_config import list_tenants, load_tenant
216 |     
217 |     tenant_ids = list_tenants()
218 |     lines = ["AVAILABLE TENANT PROFILES", "=" * 50, ""]
219 |     
220 |     for tid in tenant_ids:
221 |         tenant = load_tenant(str(tid))
222 |         lines += [
223 |             f"Profile: {tid}",
224 |             f"  Name              : {tenant.name}",
225 |             f"  Tier              : {tenant.tier}",
226 |             f"  FFIEC Category    : {tenant.ffiec_category}",
227 |             f"  Parity Threshold  : {tenant.parity_threshold_pct}%",
228 |             f"  Fee Tolerance     : ${tenant.fee_tolerance_usd:.2f}",
229 |             f"  Anomaly Sigma     : {tenant.anomaly_sigma_threshold}σ",
230 |             f"  Basel III Weight  : {tenant.basel_operational_risk_weight}%",
231 |             f"  PSD2 Jurisdiction : {'Yes' if tenant.psd2_jurisdiction else 'No'}",
232 |             f"  Max Daily Exposure: ${tenant.max_daily_exposure_usd:,.0f}",
233 |             "",
234 |         ]
235 |     
236 |     return "\n".join(lines)
237 | 
238 | 
239 | # ── Tool: get tenant profile details ──────────────────────────────────────────
240 | @mcp.tool()
241 | def get_tenant_profile(tenant_id: str = "demo_default") -> str:
242 |     """
243 |     Get detailed information about a specific tenant profile including
244 |     regulatory justifications and threshold settings.
245 |     
246 |     Args:
247 |         tenant_id: Tenant profile ID (tier1_global, tier2_regional, community_bank, demo_default).
248 |     """
249 |     from parity.tenant_config import load_tenant
250 |     
251 |     try:
252 |         tenant = load_tenant(tenant_id)
253 |     except FileNotFoundError:
254 |         return f"Tenant profile '{tenant_id}' not found. Use list_tenant_profiles() to see available profiles."
255 |     
256 |     return f"""TENANT PROFILE: {tenant_id}
257 | {"=" * 50}
258 | 
259 | BASIC INFO:
260 |   Name                  : {tenant.name}
261 |   Tier                  : {tenant.tier}
262 | 
263 | REGULATORY CLASSIFICATION:
264 |   FFIEC Category        : {tenant.ffiec_category}
265 |   Basel III Risk Weight : {tenant.basel_operational_risk_weight}%
266 |   PSD2 Jurisdiction     : {'Yes' if tenant.psd2_jurisdiction else 'No'}
267 | 
268 | PARITY THRESHOLDS:
269 |   Parity Threshold      : {tenant.parity_threshold_pct}%
270 |   Fee Tolerance         : ${tenant.fee_tolerance_usd:.2f}
271 |   Amount Tolerance      : ${tenant.amount_tolerance_usd:.2f}
272 |   Anomaly Sigma         : {tenant.anomaly_sigma_threshold}σ
273 | 
274 | RISK APPETITE:
275 |   Max Daily Exposure    : ${tenant.max_daily_exposure_usd:,.0f}
276 |   Requires CTO Signoff  : {'Yes' if tenant.requires_cto_signoff else 'No'}
277 | 
278 | USAGE:
279 |   Use this profile in analyze_cutover_readiness() by passing:
280 |   tenant_id="{tenant_id}"
281 | """
282 | 
283 | 
284 | # ── Tool: compare confidence intervals ────────────────────────────────────────
285 | @mcp.tool()
286 | def compare_confidence_intervals(successes: int, trials: int, confidence: float = 0.95) -> str:
287 |     """
288 |     Compare multiple confidence interval methods for parity analysis.
289 |     
290 |     Provides Wilson, Bootstrap, Bayesian, and Funnel plot bounds to validate
291 |     statistical robustness of parity estimates.
292 |     
293 |     Args:
294 |         successes: Number of successful parity matches
295 |         trials: Total number of transactions tested
296 |         confidence: Confidence level (default 0.95 for 95% CI)
297 |     
298 |     Returns:
299 |         Formatted comparison of all confidence interval methods
300 |     """
301 |     from parity.confidence import compare_intervals, get_interval_consensus
302 |     
303 |     intervals = compare_intervals(successes, trials, confidence)
304 |     consensus = get_interval_consensus(successes, trials, confidence)
305 |     
306 |     parity_rate = (successes / trials * 100) if trials > 0 else 0.0
307 |     
308 |     lines = [
309 |         "CONFIDENCE INTERVAL COMPARISON",
310 |         "=" * 60,
311 |         f"Sample: {successes}/{trials} matches ({parity_rate:.1f}% parity)",
312 |         f"Confidence Level: {confidence * 100:.0f}%",
313 |         "",
314 |         "METHOD COMPARISON:",
315 |         ""
316 |     ]
317 |     
318 |     # Wilson Score
319 |     w = intervals["wilson"]
320 |     lines += [
321 |         "Wilson Score (Current Method):",
322 |         f"  Interval: [{w['lower']:.2f}%, {w['upper']:.2f}%]",
323 |         f"  Width: {w['width']:.2f}%",
324 |         f"  Point Estimate: {w['point']:.2f}%",
325 |         ""
326 |     ]
327 |     
328 |     # Bootstrap
329 |     b = intervals["bootstrap"]
330 |     lines += [
331 |         "Bootstrap (Non-parametric):",
332 |         f"  Interval: [{b['lower']:.2f}%, {b['upper']:.2f}%]",
333 |         f"  Width: {b['width']:.2f}%",
334 |         f"  Point Estimate: {b['point']:.2f}%",
335 |         ""
336 |     ]
337 |     
338 |     # Bayesian
339 |     bay = intervals["bayesian"]
340 |     lines += [
341 |         "Bayesian (Beta-Binomial):",
342 |         f"  Interval: [{bay['lower']:.2f}%, {bay['upper']:.2f}%]",
343 |         f"  Width: {bay['width']:.2f}%",
344 |         f"  Point Estimate: {bay['point']:.2f}%",
345 |         ""
346 |     ]
347 |     
348 |     # Funnel Plot
349 |     f = intervals["funnel"]
350 |     lines += [
351 |         "Funnel Plot Bounds (95% target):",
352 |         f"  Expected Range: [{f['lower']:.2f}%, {f['upper']:.2f}%]",
353 |         f"  Target: {f['target']:.1f}%",
354 |         ""
355 |     ]
356 |     
357 |     # Consensus
358 |     lines += [
359 |         "CONSENSUS ANALYSIS:",
360 |         f"  Conservative Interval: [{consensus['consensus_lower']:.2f}%, {consensus['consensus_upper']:.2f}%]",
361 |         f"  Width: {consensus['consensus_width']:.2f}%",
362 |         f"  Methods Agree: {'YES' if consensus['methods_agree'] else 'NO'}",
363 |         ""
364 |     ]
365 |     
366 |     if not consensus['methods_agree']:
367 |         lines += [
368 |             "⚠️  WARNING: Significant disagreement between methods detected.",
369 |             f"   Lower bound range: {consensus['lower_range']:.2f}%",
370 |             f"   Upper bound range: {consensus['upper_range']:.2f}%",
371 |             "   Consider collecting more samples for robust estimation.",
372 |             ""
373 |         ]
374 |     
375 |     lines += [
376 |         "INTERPRETATION:",
377 |         "  - Wilson: Standard method, good for most cases",
378 |         "  - Bootstrap: Robust for small samples, no assumptions",
379 |         "  - Bayesian: Incorporates prior knowledge",
380 |         "  - Funnel: Detects outliers based on sample size",
381 |         "  - Use consensus interval for conservative decisions"
382 |     ]
383 |     
384 |     return "\n".join(lines)
385 | 
386 | 
387 | # ── Tool: check drift ──────────────────────────────────────────────────────────
388 | @mcp.tool()
389 | def check_drift(function_name: str, tenant_id: str = "demo_default") -> str:
390 |     """
391 |     Check for parity drift using CUSUM and EWMA statistical process control.
392 |     
393 |     Analyzes historical run data to detect sustained degradation in parity rates.
394 |     Useful for early warning of emerging issues before they become critical.
395 |     
396 |     Args:
397 |         function_name: Payment function to analyze (e.g., "Domestic Wire Transfer")
398 |         tenant_id: Tenant profile for context (default "demo_default")
399 |     
400 |     Returns:
401 |         Drift detection summary with CUSUM, EWMA, and recommendations
402 |     """
403 |     from parity.drift_detection import DriftDetector
404 |     
405 |     detector = DriftDetector()
406 |     summary = detector.get_drift_summary(function_name, tenant_id)
407 |     
408 |     lines = [
409 |         f"DRIFT DETECTION: {function_name}",
410 |         "=" * 60,
411 |         f"Tenant: {tenant_id}",
412 |         f"Total Runs Analyzed: {summary['total_runs']}",
413 |         ""
414 |     ]
415 |     
416 |     if summary['total_runs'] < 5:
417 |         lines += [
418 |             "⚠️  INSUFFICIENT DATA",
419 |             "   Need at least 5 historical runs for drift detection.",
420 |             "   Continue running analyses to build history.",
421 |             ""
422 |         ]
423 |         return "\n".join(lines)
424 |     
425 |     # Overall status
426 |     drift_detected = summary['drift_detected']
427 |     trend = summary['trend']
428 |     
429 |     if drift_detected:
430 |         lines += [
431 |             "🚨 DRIFT DETECTED",
432 |             f"   Trend: {trend}",
433 |             ""
434 |         ]
435 |     else:
436 |         lines += [
437 |             "✓ NO DRIFT DETECTED",
438 |             f"   Trend: {trend}",
439 |             ""
440 |         ]
441 |     
442 |     # CUSUM results
443 |     cusum = summary['cusum']
444 |     lines += [
445 |         "CUSUM (Cumulative Sum) Analysis:",
446 |         f"  Current Value: {cusum['cusum_value']:.2f}",
447 |         f"  Threshold: {cusum['threshold']:.2f}",
448 |         f"  Severity: {cusum['severity']}",
449 |         f"  Status: {'ALARM' if cusum['drift_detected'] else 'OK'}",
450 |         ""
451 |     ]
452 |     
453 |     # EWMA results
454 |     ewma = summary['ewma']
455 |     lines += [
456 |         "EWMA (Exponentially Weighted Moving Average):",
457 |         f"  Current Value: {ewma['ewma_value']:.2f}%",
458 |         f"  Mean Rate: {ewma['mean_rate']:.2f}%",
459 |         f"  Control Limits: [{ewma['lower_limit']:.2f}%, {ewma['upper_limit']:.2f}%]",
460 |         f"  Severity: {ewma['severity']}",
461 |         f"  Status: {'ALARM' if ewma['drift_detected'] else 'OK'}",
462 |         ""
463 |     ]
464 |     
465 |     # Recent history
466 |     if summary['recent_history']:
467 |         lines += ["RECENT HISTORY (last 5 runs):"]
468 |         for i, run in enumerate(summary['recent_history'], 1):
469 |             lines.append(f"  {i}. {run['parity_rate_pct']:.1f}% parity ({run['verdict']})")
470 |         lines.append("")
471 |     
472 |     # Recommendation
473 |     lines += [
474 |         "RECOMMENDATION:",
475 |         f"  {summary['recommendation']}",
476 |         ""
477 |     ]
478 |     
479 |     return "\n".join(lines)
480 | 
481 | 
482 | # ── Tool: assess compliance ────────────────────────────────────────────────────
483 | @mcp.tool()
484 | def assess_compliance(tenant_id: str = "demo_default") -> str:
485 |     """
486 |     Assess regulatory compliance across FFIEC, Basel III, PSD2, SWIFT gpi, and SOX.
487 |     
488 |     Evaluates current system configuration and recent analysis results against
489 |     12 regulatory requirements. Generates compliance score and attestation.
490 |     
491 |     Args:
492 |         tenant_id: Tenant profile to assess (default "demo_default")
493 |     
494 |     Returns:
495 |         Compliance assessment with scores and attestation
496 |     """
497 |     from parity.compliance import ComplianceFramework
498 |     from parity.tenant_config import load_tenant
499 |     
500 |     # Load tenant profile
501 |     tenant = load_tenant(tenant_id)
502 |     tenant_dict = tenant.to_dict()
503 |     
504 |     # Create mock scores for demonstration (in production, use actual latest run)
505 |     mock_scores = [
506 |         {
507 |             "function": "Domestic Wire Transfer",
508 |             "parity_rate_pct": 100.0,
509 |             "total_transactions": 80,
510 |             "anomaly_count": 0,
511 |             "avg_fee_diff_usd": 0.0001,
512 |             "verdict": "SAFE_TO_CUT"
513 |         },
514 |         {
515 |             "function": "International Wire Transfer",
516 |             "parity_rate_pct": 0.0,
517 |             "total_transactions": 80,
518 |             "anomaly_count": 15,
519 |             "avg_fee_diff_usd": 794.50,
520 |             "verdict": "DO_NOT_CUT"
521 |         }
522 |     ]
523 |     
524 |     # Assess compliance
525 |     framework = ComplianceFramework()
526 |     assessments = framework.assess_compliance(mock_scores, tenant_dict, drift_summary=None)
527 |     compliance_score = framework.get_compliance_score(assessments)
528 |     
529 |     lines = [
530 |         "REGULATORY COMPLIANCE ASSESSMENT",
531 |         "=" * 60,
532 |         f"Tenant: {tenant_id} ({tenant.name})",
533 |         f"Overall Score: {compliance_score['overall_score']:.1f}/100",
534 |         ""
535 |     ]
536 |     
537 |     # Framework scores
538 |     lines += ["FRAMEWORK SCORES:", ""]
539 |     for framework_name, data in compliance_score['framework_scores'].items():
540 |         status_icon = "✓" if data['failed'] == 0 else "⚠️" if data['failed'] < data['total_requirements'] else "✗"
541 |         lines += [
542 |             f"{status_icon} {framework_name}:",
543 |             f"   Score: {data['score']:.1f}/100",
544 |             f"   Passed: {data['passed']}/{data['total_requirements']}",
545 |             f"   Failed: {data['failed']}",
546 |             ""
547 |         ]
548 |     
549 |     # Critical failures
550 |     if compliance_score['critical_failures'] > 0:
551 |         lines += [
552 |             f"🚨 CRITICAL FAILURES: {compliance_score['critical_failures']}",
553 |             "   Cutover NOT RECOMMENDED until resolved.",
554 |             ""
555 |         ]
556 |     else:
557 |         lines += [
558 |             "✓ No critical failures detected.",
559 |             "  Cutover may proceed subject to risk assessment.",
560 |             ""
561 |         ]
562 |     
563 |     # Failed requirements
564 |     failed = [a for a in assessments if a.status == "FAIL"]
565 |     if failed:
566 |         lines += ["FAILED REQUIREMENTS:", ""]
567 |         for assessment in failed:
568 |             lines += [
569 |                 f"  {assessment.requirement.requirement_id}: {assessment.requirement.title}",
570 |                 f"    Framework: {assessment.requirement.framework.value}",
571 |                 f"    Severity: {assessment.requirement.severity}",
572 |                 f"    Evidence: {assessment.evidence}",
573 |                 ""
574 |             ]
575 |     
576 |     # Recommendations
577 |     all_recommendations = []
578 |     for assessment in assessments:
579 |         all_recommendations.extend(assessment.recommendations)
580 |     
581 |     if all_recommendations:
582 |         lines += ["RECOMMENDATIONS:", ""]
583 |         for i, rec in enumerate(set(all_recommendations), 1):
584 |             lines.append(f"  {i}. {rec}")
585 |         lines.append("")
586 |     
587 |     lines += [
588 |         "NOTE: This is a live assessment based on current configuration.",
589 |         "      Run analyze_cutover_readiness() for full analysis with actual data."
590 |     ]
591 |     
592 |     return "\n".join(lines)
593 | 
594 | 
595 | if __name__ == "__main__":
596 |     mcp.run()
</content>
</file>
<file><path>audit/pdf_report.py</path>
<content lines="1-499">
  1 | """
  2 | Generates a regulator-grade cutover audit PDF.
  3 | Designed to look like a real compliance sign-off document.
  4 | """
  5 | 
  6 | from datetime import datetime, timezone
  7 | from io import BytesIO
  8 | 
  9 | from reportlab.lib import colors
 10 | from reportlab.lib.pagesizes import A4
 11 | from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 12 | from reportlab.lib.units import mm
 13 | from reportlab.platypus import (
 14 |     BaseDocTemplate,
 15 |     Frame,
 16 |     PageTemplate,
 17 |     Paragraph,
 18 |     Spacer,
 19 |     Table,
 20 |     TableStyle,
 21 |     HRFlowable,
 22 |     KeepTogether,
 23 | )
 24 | from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
 25 | 
 26 | # ── Colours ───────────────────────────────────────────────────────────────────
 27 | C_DARK = colors.HexColor("#0e1117")
 28 | C_BRAND = colors.HexColor("#6366f1")
 29 | C_GREEN = colors.HexColor("#00C851")
 30 | C_YELLOW = colors.HexColor("#FFBB33")
 31 | C_ORANGE = colors.HexColor("#FF8800")
 32 | C_RED = colors.HexColor("#FF4444")
 33 | C_LIGHT_GREY = colors.HexColor("#f3f4f6")
 34 | C_MID_GREY = colors.HexColor("#6b7280")
 35 | C_BORDER = colors.HexColor("#e5e7eb")
 36 | 
 37 | VERDICT_COLOUR = {
 38 |     "SAFE_TO_CUT": C_GREEN,
 39 |     "CUT_WITH_MONITORING": C_YELLOW,
 40 |     "HOLD_INVESTIGATE": C_ORANGE,
 41 |     "DO_NOT_CUT": C_RED,
 42 | }
 43 | 
 44 | W, H = A4
 45 | 
 46 | 
 47 | def _styles():
 48 |     base = getSampleStyleSheet()
 49 |     return {
 50 |         "title": ParagraphStyle("title", parent=base["Normal"],
 51 |                                 fontSize=22, leading=28,
 52 |                                 textColor=C_DARK, fontName="Helvetica-Bold"),
 53 |         "subtitle": ParagraphStyle("subtitle", parent=base["Normal"],
 54 |                                    fontSize=11, leading=16,
 55 |                                    textColor=C_MID_GREY, fontName="Helvetica"),
 56 |         "section": ParagraphStyle("section", parent=base["Normal"],
 57 |                                   fontSize=13, leading=18, spaceBefore=14, spaceAfter=4,
 58 |                                   textColor=C_BRAND, fontName="Helvetica-Bold"),
 59 |         "body": ParagraphStyle("body", parent=base["Normal"],
 60 |                                fontSize=9, leading=14,
 61 |                                textColor=C_DARK, fontName="Helvetica"),
 62 |         "small": ParagraphStyle("small", parent=base["Normal"],
 63 |                                 fontSize=8, leading=12,
 64 |                                 textColor=C_MID_GREY, fontName="Helvetica"),
 65 |         "bold": ParagraphStyle("bold", parent=base["Normal"],
 66 |                                fontSize=9, leading=14,
 67 |                                textColor=C_DARK, fontName="Helvetica-Bold"),
 68 |         "centre": ParagraphStyle("centre", parent=base["Normal"],
 69 |                                  fontSize=9, leading=14, alignment=TA_CENTER,
 70 |                                  textColor=C_DARK, fontName="Helvetica"),
 71 |     }
 72 | 
 73 | 
 74 | def _header_footer(canvas, doc):
 75 |     canvas.saveState()
 76 |     # Header bar
 77 |     canvas.setFillColor(C_BRAND)
 78 |     canvas.rect(0, H - 18 * mm, W, 18 * mm, fill=1, stroke=0)
 79 |     canvas.setFillColor(colors.white)
 80 |     canvas.setFont("Helvetica-Bold", 11)
 81 |     canvas.drawString(20 * mm, H - 11 * mm, "BOB THE JUDGE")
 82 |     canvas.setFont("Helvetica", 9)
 83 |     canvas.drawRightString(W - 20 * mm, H - 11 * mm, "MIGRATION CUTOVER AUDIT REPORT")
 84 |     # Footer
 85 |     canvas.setFillColor(C_MID_GREY)
 86 |     canvas.setFont("Helvetica", 7)
 87 |     canvas.drawString(20 * mm, 10 * mm,
 88 |                       "CONFIDENTIAL — For internal migration governance and regulatory review only.")
 89 |     canvas.drawRightString(W - 20 * mm, 10 * mm, f"Page {doc.page}")
 90 |     canvas.restoreState()
 91 | 
 92 | 
 93 | def generate_pdf(scores: list[dict], results: list[dict], run_ts: datetime | None = None, bob_session_id: str | None = None, tenant_profile: dict | None = None) -> bytes:
 94 |     if run_ts is None:
 95 |         run_ts = datetime.now(timezone.utc)
 96 | 
 97 |     buf = BytesIO()
 98 |     s = _styles()
 99 | 
100 |     doc = BaseDocTemplate(
101 |         buf,
102 |         pagesize=A4,
103 |         leftMargin=20 * mm,
104 |         rightMargin=20 * mm,
105 |         topMargin=28 * mm,
106 |         bottomMargin=22 * mm,
107 |     )
108 |     frame = Frame(doc.leftMargin, doc.bottomMargin,
109 |                   doc.width, doc.height, id="main")
110 |     doc.addPageTemplates([PageTemplate(id="main", frames=frame,
111 |                                        onPage=_header_footer)])
112 | 
113 |     story = []
114 | 
115 |     # ── Cover block ────────────────────────────────────────────────────────
116 |     story.append(Spacer(1, 8 * mm))
117 |     story.append(Paragraph("Migration Cutover Audit Report", s["title"]))
118 |     story.append(Spacer(1, 2 * mm))
119 |     story.append(Paragraph(
120 |         f"Generated by Bob the Judge &nbsp;·&nbsp; "
121 |         f"{run_ts.strftime('%d %B %Y, %H:%M UTC')} &nbsp;·&nbsp; "
122 |         f"Banking Payment Processing Domain",
123 |         s["subtitle"],
124 |     ))
125 |     story.append(Spacer(1, 4 * mm))
126 |     story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
127 |     story.append(Spacer(1, 4 * mm))
128 | 
129 |     # ── Executive summary ──────────────────────────────────────────────────
130 |     total_txns = sum(s_["total_transactions"] for s_ in scores)
131 |     overall_parity = (
132 |         sum(s_["parity_rate_pct"] * s_["total_transactions"] for s_ in scores)
133 |         / max(total_txns, 1)
134 |     )
135 |     safe_count = sum(1 for s_ in scores if s_["verdict"] == "SAFE_TO_CUT")
136 |     blocked_count = sum(1 for s_ in scores if s_["verdict"] == "DO_NOT_CUT")
137 | 
138 |     summary_data = [
139 |         ["Metric", "Value"],
140 |         ["Total Transactions Analysed", f"{total_txns:,}"],
141 |         ["Overall Parity Rate", f"{overall_parity:.1f}%"],
142 |         ["Functions Cleared for Cutover", f"{safe_count} of {len(scores)}"],
143 |         ["Functions Blocked", f"{blocked_count}"],
144 |         ["Analysis Timestamp", run_ts.strftime("%Y-%m-%d %H:%M:%S UTC")],
145 |         ["System Under Test", "Banking Payment Processor (Legacy → Modern)"],
146 |         ["Bob Session ID", bob_session_id or "—"],
147 |     ]
148 | 
149 |     story.append(Paragraph("Executive Summary", s["section"]))
150 |     
151 |     # Add tenant profile section if provided
152 |     if tenant_profile:
153 |         story.append(Spacer(1, 2 * mm))
154 |         story.append(Paragraph("Tenant Risk Profile", s["bold"]))
155 |         story.append(Spacer(1, 1 * mm))
156 |         
157 |         tenant_data = [
158 |             ["Profile Attribute", "Value"],
159 |             ["Tenant ID", tenant_profile.get("tenant_id", "—")],
160 |             ["Institution Name", tenant_profile.get("name", "—")],
161 |             ["FFIEC Category", tenant_profile.get("ffiec_category", "—")],
162 |             ["Parity Threshold", f"{tenant_profile.get('parity_threshold_pct', 95)}%"],
163 |             ["Fee Tolerance", f"${tenant_profile.get('fee_tolerance_usd', 0.02):.2f}"],
164 |             ["Anomaly Sigma Threshold", f"{tenant_profile.get('anomaly_sigma_threshold', 2.0)}σ"],
165 |             ["Basel III Risk Weight", f"{tenant_profile.get('basel_operational_risk_weight', 15)}%"],
166 |             ["PSD2 Jurisdiction", "Yes" if tenant_profile.get("psd2_jurisdiction") else "No"],
167 |         ]
168 |         
169 |         t_tenant = Table(tenant_data, colWidths=[90 * mm, 75 * mm])
170 |         t_tenant.setStyle(TableStyle([
171 |             ("BACKGROUND", (0, 0), (-1, 0), C_BRAND),
172 |             ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
173 |             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
174 |             ("FONTSIZE", (0, 0), (-1, -1), 8),
175 |             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_LIGHT_GREY, colors.white]),
176 |             ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
177 |             ("LEFTPADDING", (0, 0), (-1, -1), 8),
178 |             ("RIGHTPADDING", (0, 0), (-1, -1), 8),
179 |             ("TOPPADDING", (0, 0), (-1, -1), 4),
180 |             ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
181 |         ]))
182 |         story.append(t_tenant)
183 |         story.append(Spacer(1, 3 * mm))
184 |         
185 |         # Add regulatory justification note
186 |         story.append(Paragraph(
187 |             "<b>Regulatory Basis:</b> Thresholds calibrated per FFIEC IT Handbook "
188 |             "(risk commensurate with institution size/complexity), Basel III Pillar 2 "
189 |             "(institution-specific operational risk assessment), and PSD2 requirements "
190 |             "where applicable.",
191 |             s["small"]
192 |         ))
193 |         story.append(Spacer(1, 4 * mm))
194 |     t = Table(summary_data, colWidths=[90 * mm, 75 * mm])
195 |     t.setStyle(TableStyle([
196 |         ("BACKGROUND", (0, 0), (-1, 0), C_BRAND),
197 |         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
198 |         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
199 |         ("FONTSIZE", (0, 0), (-1, -1), 9),
200 |         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_LIGHT_GREY, colors.white]),
201 |         ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
202 |         ("LEFTPADDING", (0, 0), (-1, -1), 8),
203 |         ("RIGHTPADDING", (0, 0), (-1, -1), 8),
204 |         ("TOPPADDING", (0, 0), (-1, -1), 5),
205 |         ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
206 |     ]))
207 |     story.append(t)
208 |     story.append(Spacer(1, 6 * mm))
209 | 
210 |     # ── Function scorecards ────────────────────────────────────────────────
211 |     story.append(Paragraph("Function-Level Cutover Verdicts", s["section"]))
212 | 
213 |     header = ["Payment Function", "Transactions", "Parity %", "Score", "Verdict",
214 |               "Avg Fee Diff", "Latency Gain"]
215 |     rows = [header]
216 |     for sc in scores:
217 |         rows.append([
218 |             sc["function"],
219 |             str(sc["total_transactions"]),
220 |             f"{sc['parity_rate_pct']:.1f}%",
221 |             f"{sc['readiness_score']:.1f}",
222 |             sc["verdict"].replace("_", " "),
223 |             f"${sc['avg_fee_diff_usd']:.4f}",
224 |             f"{sc['avg_latency_improvement_pct']:+.1f}%",
225 |         ])
226 | 
227 |     col_w = [55 * mm, 22 * mm, 18 * mm, 15 * mm, 32 * mm, 22 * mm, 22 * mm]
228 |     t2 = Table(rows, colWidths=col_w)
229 |     style_cmds = [
230 |         ("BACKGROUND", (0, 0), (-1, 0), C_DARK),
231 |         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
232 |         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
233 |         ("FONTSIZE", (0, 0), (-1, -1), 8),
234 |         ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_LIGHT_GREY, colors.white]),
235 |         ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
236 |         ("LEFTPADDING", (0, 0), (-1, -1), 6),
237 |         ("RIGHTPADDING", (0, 0), (-1, -1), 6),
238 |         ("TOPPADDING", (0, 0), (-1, -1), 4),
239 |         ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
240 |         ("ALIGN", (1, 0), (-1, -1), "CENTER"),
241 |     ]
242 |     for i, sc in enumerate(scores, start=1):
243 |         c = VERDICT_COLOUR.get(sc["verdict"], C_MID_GREY)
244 |         style_cmds.append(("TEXTCOLOR", (4, i), (4, i), c))
245 |         style_cmds.append(("FONTNAME", (4, i), (4, i), "Helvetica-Bold"))
246 |     t2.setStyle(TableStyle(style_cmds))
247 |     story.append(t2)
248 |     story.append(Spacer(1, 6 * mm))
249 | 
250 |     # ── Divergence detail ──────────────────────────────────────────────────
251 |     divergent = [r for r in results if not r["parity"]]
252 |     story.append(Paragraph(
253 |         f"Divergence Detail ({len(divergent)} divergent transactions)", s["section"]
254 |     ))
255 | 
256 |     if divergent:
257 |         div_header = ["Transaction ID", "Type", "Amount", "Field", "Legacy", "Modern", "Severity"]
258 |         div_rows = [div_header]
259 |         for r in divergent[:30]:
260 |             for d in r["divergences"]:
261 |                 div_rows.append([
262 |                     r["transaction_id"],
263 |                     r["transaction_type"].title(),
264 |                     f"${r['amount']:,.2f} {r['currency']}",
265 |                     d["field"],
266 |                     str(d["legacy"])[:12],
267 |                     str(d["modern"])[:12],
268 |                     d["severity"],
269 |                 ])
270 |         if len(divergent) > 30:
271 |             div_rows.append(["…", f"+ {len(divergent) - 30} more", "", "", "", "", ""])
272 | 
273 |         col_w2 = [30 * mm, 22 * mm, 28 * mm, 25 * mm, 20 * mm, 20 * mm, 20 * mm]
274 |         t3 = Table(div_rows, colWidths=col_w2)
275 |         sev_style = [
276 |             ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e2130")),
277 |             ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
278 |             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
279 |             ("FONTSIZE", (0, 0), (-1, -1), 7),
280 |             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_LIGHT_GREY, colors.white]),
281 |             ("GRID", (0, 0), (-1, -1), 0.4, C_BORDER),
282 |             ("LEFTPADDING", (0, 0), (-1, -1), 5),
283 |             ("RIGHTPADDING", (0, 0), (-1, -1), 5),
284 |             ("TOPPADDING", (0, 0), (-1, -1), 3),
285 |             ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
286 |         ]
287 |         for i, r in enumerate(divergent[:30], start=1):
288 |             for d in r["divergences"]:
289 |                 sev = d["severity"]
290 |                 c = {"CRITICAL": C_RED, "HIGH": C_ORANGE, "MEDIUM": C_YELLOW}.get(sev, C_MID_GREY)
291 |                 sev_style.append(("TEXTCOLOR", (6, i), (6, i), c))
292 |                 sev_style.append(("FONTNAME", (6, i), (6, i), "Helvetica-Bold"))
293 |         t3.setStyle(TableStyle(sev_style))
294 |         story.append(t3)
295 |     else:
296 |         story.append(Paragraph("No divergences detected. All functions at 100% parity.", s["body"]))
297 | 
298 |     story.append(Spacer(1, 6 * mm))
299 | 
300 |     # ── Recommendations ────────────────────────────────────────────────────
301 |     story.append(Paragraph("Bob the Judge — Cutover Recommendation", s["section"]))
302 | 
303 |     for sc in scores:
304 |         verdict = sc["verdict"]
305 |         colour = VERDICT_COLOUR.get(verdict, C_MID_GREY)
306 |         label = verdict.replace("_", " ")
307 | 
308 |         if verdict == "SAFE_TO_CUT":
309 |             action = (
310 |                 f"<b>{sc['function']}</b> has achieved {sc['parity_rate_pct']:.1f}% parity "
311 |                 f"across {sc['total_transactions']} transactions with a readiness score of "
312 |                 f"{sc['readiness_score']:.1f}/100. <b>Approved for immediate cutover.</b> "
313 |                 f"No further parallel run required."
314 |             )
315 |         elif verdict == "CUT_WITH_MONITORING":
316 |             action = (
317 |                 f"<b>{sc['function']}</b> shows {sc['parity_rate_pct']:.1f}% parity "
318 |                 f"(score {sc['readiness_score']:.1f}/100). Cutover is permitted with "
319 |                 f"real-time monitoring. Recommend 24-hour observation window post-cutover."
320 |             )
321 |         elif verdict == "HOLD_INVESTIGATE":
322 |             action = (
323 |                 f"<b>{sc['function']}</b> at {sc['parity_rate_pct']:.1f}% parity "
324 |                 f"(score {sc['readiness_score']:.1f}/100). Divergences require investigation "
325 |                 f"before cutover. Extend parallel run by minimum 7 days."
326 |             )
327 |         else:
328 |             action = (
329 |                 f"<b>{sc['function']}</b> at {sc['parity_rate_pct']:.1f}% parity "
330 |                 f"(score {sc['readiness_score']:.1f}/100). <b>Cutover blocked.</b> "
331 |                 f"Critical divergences detected — escalate to migration lead and compliance team."
332 |             )
333 | 
334 |         rec_data = [[f"  {label}", Paragraph(action, s["body"])]]
335 |         t_rec = Table(rec_data, colWidths=[38 * mm, 130 * mm])
336 |         t_rec.setStyle(TableStyle([
337 |             ("BACKGROUND", (0, 0), (0, 0), colour),
338 |             ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
339 |             ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
340 |             ("FONTSIZE", (0, 0), (0, 0), 8),
341 |             ("ALIGN", (0, 0), (0, 0), "CENTER"),
342 |             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
343 |             ("BACKGROUND", (1, 0), (1, 0), colors.white),
344 |             ("BOX", (0, 0), (-1, -1), 0.5, C_BORDER),
345 |             ("LEFTPADDING", (0, 0), (-1, -1), 8),
346 |             ("RIGHTPADDING", (0, 0), (-1, -1), 8),
347 |             ("TOPPADDING", (0, 0), (-1, -1), 8),
348 |             ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
349 |         ]))
350 |         story.append(KeepTogether([t_rec, Spacer(1, 3 * mm)]))
351 | 
352 |     # ── Regulatory Compliance Attestation ──────────────────────────────────
353 |     if tenant_profile:
354 |         story.append(Spacer(1, 8 * mm))
355 |         story.append(Paragraph("Regulatory Compliance Attestation", s["section"]))
356 |         
357 |         # Generate compliance assessment
358 |         from parity.compliance import ComplianceFramework
359 |         framework = ComplianceFramework()
360 |         assessments = framework.assess_compliance(scores, tenant_profile, drift_summary=None)
361 |         compliance_score = framework.get_compliance_score(assessments)
362 |         
363 |         # Overall compliance score
364 |         score_color = C_GREEN if compliance_score['overall_score'] >= 90 else C_YELLOW if compliance_score['overall_score'] >= 70 else C_RED
365 |         
366 |         compliance_summary = [
367 |             ["Compliance Metric", "Result"],
368 |             ["Overall Compliance Score", f"{compliance_score['overall_score']:.1f}/100"],
369 |             ["Total Requirements Assessed", str(compliance_score['total_requirements'])],
370 |             ["Critical Failures", str(compliance_score['critical_failures'])],
371 |         ]
372 |         
373 |         t_comp = Table(compliance_summary, colWidths=[90 * mm, 75 * mm])
374 |         t_comp.setStyle(TableStyle([
375 |             ("BACKGROUND", (0, 0), (-1, 0), C_BRAND),
376 |             ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
377 |             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
378 |             ("FONTSIZE", (0, 0), (-1, -1), 9),
379 |             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_LIGHT_GREY, colors.white]),
380 |             ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
381 |             ("LEFTPADDING", (0, 0), (-1, -1), 8),
382 |             ("RIGHTPADDING", (0, 0), (-1, -1), 8),
383 |             ("TOPPADDING", (0, 0), (-1, -1), 5),
384 |             ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
385 |             ("TEXTCOLOR", (1, 1), (1, 1), score_color),
386 |             ("FONTNAME", (1, 1), (1, 1), "Helvetica-Bold"),
387 |         ]))
388 |         story.append(t_comp)
389 |         story.append(Spacer(1, 4 * mm))
390 |         
391 |         # Framework breakdown
392 |         framework_rows = [["Regulatory Framework", "Score", "Status"]]
393 |         for framework_name, data in compliance_score['framework_scores'].items():
394 |             status = "PASS" if data['failed'] == 0 else "PARTIAL" if data['failed'] < data['total_requirements'] else "FAIL"
395 |             status_color = C_GREEN if status == "PASS" else C_YELLOW if status == "PARTIAL" else C_RED
396 |             framework_rows.append([
397 |                 framework_name,
398 |                 f"{data['score']:.1f}/100",
399 |                 status
400 |             ])
401 |         
402 |         t_frameworks = Table(framework_rows, colWidths=[90 * mm, 40 * mm, 35 * mm])
403 |         style_cmds_fw = [
404 |             ("BACKGROUND", (0, 0), (-1, 0), C_DARK),
405 |             ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
406 |             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
407 |             ("FONTSIZE", (0, 0), (-1, -1), 8),
408 |             ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_LIGHT_GREY, colors.white]),
409 |             ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
410 |             ("LEFTPADDING", (0, 0), (-1, -1), 6),
411 |             ("RIGHTPADDING", (0, 0), (-1, -1), 6),
412 |             ("TOPPADDING", (0, 0), (-1, -1), 4),
413 |             ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
414 |             ("ALIGN", (1, 0), (-1, -1), "CENTER"),
415 |         ]
416 |         
417 |         # Color-code status column
418 |         for i in range(1, len(framework_rows)):
419 |             status = framework_rows[i][2]
420 |             status_color = C_GREEN if status == "PASS" else C_YELLOW if status == "PARTIAL" else C_RED
421 |             style_cmds_fw.append(("TEXTCOLOR", (2, i), (2, i), status_color))
422 |             style_cmds_fw.append(("FONTNAME", (2, i), (2, i), "Helvetica-Bold"))
423 |         
424 |         t_frameworks.setStyle(TableStyle(style_cmds_fw))
425 |         story.append(t_frameworks)
426 |         story.append(Spacer(1, 4 * mm))
427 |         
428 |         # Attestation statement
429 |         if compliance_score['critical_failures'] > 0:
430 |             attestation_text = (
431 |                 f"<b>COMPLIANCE WARNING:</b> {compliance_score['critical_failures']} critical "
432 |                 f"requirement(s) failed. This migration cutover does NOT meet all regulatory "
433 |                 f"requirements. Immediate remediation required before proceeding. "
434 |                 f"Escalate to compliance team and migration governance board."
435 |             )
436 |             attestation_color = C_RED
437 |         else:
438 |             attestation_text = (
439 |                 f"<b>COMPLIANCE ATTESTATION:</b> All critical regulatory requirements satisfied. "
440 |                 f"Overall compliance score: {compliance_score['overall_score']:.1f}/100. "
441 |                 f"This migration cutover meets FFIEC, Basel III, PSD2, SWIFT gpi, and SOX 404 "
442 |                 f"requirements based on automated assessment. Manual review and sign-off required."
443 |             )
444 |             attestation_color = C_GREEN
445 |         
446 |         attestation_table = [[Paragraph(attestation_text, s["body"])]]
447 |         t_att = Table(attestation_table, colWidths=[165 * mm])
448 |         t_att.setStyle(TableStyle([
449 |             ("BACKGROUND", (0, 0), (-1, -1), C_LIGHT_GREY),
450 |             ("BOX", (0, 0), (-1, -1), 2, attestation_color),
451 |             ("LEFTPADDING", (0, 0), (-1, -1), 10),
452 |             ("RIGHTPADDING", (0, 0), (-1, -1), 10),
453 |             ("TOPPADDING", (0, 0), (-1, -1), 10),
454 |             ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
455 |         ]))
456 |         story.append(t_att)
457 |         story.append(Spacer(1, 2 * mm))
458 |         
459 |         story.append(Paragraph(
460 |             "<b>Note:</b> This compliance assessment is generated automatically based on system "
461 |             "configuration and analysis results. It does not constitute legal advice. "
462 |             "Consult with legal and compliance teams before making cutover decisions.",
463 |             s["small"]
464 |         ))
465 | 
466 |     # ── Sign-off block ─────────────────────────────────────────────────────
467 |     story.append(Spacer(1, 8 * mm))
468 |     story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
469 |     story.append(Spacer(1, 4 * mm))
470 | 
471 |     signoff_data = [
472 |         ["Migration Lead", "Compliance Officer", "CTO Sign-off"],
473 |         ["", "", ""],
474 |         ["Signature: _______________", "Signature: _______________", "Signature: _______________"],
475 |         ["Date: _______________", "Date: _______________", "Date: _______________"],
476 |     ]
477 |     t_sign = Table(signoff_data, colWidths=[55 * mm, 55 * mm, 55 * mm])
478 |     t_sign.setStyle(TableStyle([
479 |         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
480 |         ("FONTSIZE", (0, 0), (-1, -1), 8),
481 |         ("TEXTCOLOR", (0, 0), (-1, 0), C_DARK),
482 |         ("TEXTCOLOR", (0, 2), (-1, -1), C_MID_GREY),
483 |         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
484 |         ("TOPPADDING", (0, 0), (-1, -1), 6),
485 |         ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
486 |         ("LINEABOVE", (0, 0), (-1, 0), 0.5, C_BRAND),
487 |     ]))
488 |     story.append(t_sign)
489 | 
490 |     story.append(Spacer(1, 4 * mm))
491 |     story.append(Paragraph(
492 |         "This report was generated automatically by Bob the Judge, an IBM Bob-powered migration "
493 |         "cutover decision system. It constitutes a machine-generated audit artefact and must be "
494 |         "countersigned by authorised personnel before use in regulatory submissions.",
495 |         s["small"],
496 |     ))
497 | 
498 |     doc.build(story)
499 |     return buf.getvalue()
</content>
</file>
<file><path>dashboard.py</path>
<content lines="1-200">
  1 | import asyncio
  2 | import time
  3 | from datetime import datetime, timezone
  4 | import streamlit as st
  5 | import pandas as pd
  6 | import plotly.graph_objects as go
  7 | import plotly.express as px
  8 | from parity.traffic_generator import run_batch
  9 | from parity.parity_engine import analyse_batch, flag_anomalies
 10 | from parity.scoring import score_results
 11 | from parity.tenant_config import load_tenant, list_tenants, get_default_tenant
 12 | from audit.pdf_report import generate_pdf
 13 | from bob.client import ask_bob
 14 | 
 15 | st.set_page_config(
 16 |     page_title="Bob the Judge — IBM Migration Advisor",
 17 |     page_icon="assets/gavel.svg",
 18 |     layout="wide",
 19 |     initial_sidebar_state="expanded",
 20 | )
 21 | 
 22 | # ── IBM Carbon Design System CSS ──────────────────────────────────────────────
 23 | st.markdown("""
 24 | <style>
 25 | @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
 26 | 
 27 | html, body, [class*="css"] {
 28 |     font-family: 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif;
 29 | }
 30 | 
 31 | .stApp { background-color: #161616; }
 32 | section[data-testid="stSidebar"] { background-color: #262626; }
 33 | 
 34 | #MainMenu, footer, header { visibility: hidden; }
 35 | [data-testid="collapsedControl"] { visibility: visible !important; }
 36 | .block-container { padding-top: 0 !important; max-width: 100% !important; }
 37 | 
 38 | .ibm-topbar {
 39 |     background: #0f62fe;
 40 |     padding: 0 45px;
 41 |     height: 67px;
 42 |     display: flex;
 43 |     align-items: center;
 44 |     justify-content: space-between;
 45 |     margin-bottom: 0;
 46 | }
 47 | .ibm-topbar-left { display: flex; align-items: center; gap: 22px; }
 48 | .ibm-logo { font-family: 'IBM Plex Sans', sans-serif; font-weight: 600; font-size: 25px; color: white; letter-spacing: 3px; }
 49 | .ibm-product-name { font-family: 'IBM Plex Sans', sans-serif; font-size: 20px; color: rgba(255,255,255,0.8); border-left: 1px solid rgba(255,255,255,0.35); padding-left: 22px; }
 50 | .ibm-topbar-right { font-family: 'IBM Plex Mono', monospace; font-size: 15px; color: rgba(255,255,255,0.7); }
 51 | 
 52 | .ibm-section-header {
 53 |     font-family: 'IBM Plex Sans', sans-serif;
 54 |     font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
 55 |     color: #8d8d8d; padding: 24px 0 8px 0; border-bottom: 1px solid #393939; margin-bottom: 16px;
 56 | }
 57 | 
 58 | .kpi-tile { background: #262626; border-top: 3px solid #0f62fe; padding: 20px 24px; min-height: 96px; }
 59 | .kpi-label { font-size: 12px; color: #8d8d8d; font-weight: 400; margin-bottom: 6px; letter-spacing: 0.16px; }
 60 | .kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 32px; font-weight: 300; color: #f4f4f4; line-height: 1; }
 61 | .kpi-sub { font-size: 11px; color: #6f6f6f; margin-top: 4px; }
 62 | 
 63 | .verdict-card { background: #262626; border: 1px solid #393939; padding: 0; overflow: hidden; }
 64 | .verdict-card-header { padding: 12px 16px; border-bottom: 1px solid #393939; }
 65 | .verdict-card-fn { font-size: 11px; color: #8d8d8d; font-weight: 500; letter-spacing: 0.32px; text-transform: uppercase; margin-bottom: 2px; }
 66 | .verdict-card-score { font-family: 'IBM Plex Mono', monospace; font-size: 48px; font-weight: 300; line-height: 1; }
 67 | .verdict-card-body { padding: 12px 16px; }
 68 | .verdict-tag { display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: 0.16px; padding: 2px 8px; margin-bottom: 10px; }
 69 | .verdict-stat { font-size: 12px; color: #c6c6c6; line-height: 1.8; font-family: 'IBM Plex Sans', sans-serif; }
 70 | .verdict-stat span { font-family: 'IBM Plex Mono', monospace; color: #f4f4f4; }
 71 | .ci-band { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #6f6f6f; margin-top: 6px; border-top: 1px solid #393939; padding-top: 6px; }
 72 | 
 73 | .diff-card {
 74 |     background: #1c1c1c;
 75 |     border: 1px solid #393939;
 76 |     margin-bottom: 12px;
 77 |     overflow: hidden;
 78 | }
 79 | .diff-card-header {
 80 |     background: #262626;
 81 |     padding: 8px 16px;
 82 |     border-bottom: 1px solid #393939;
 83 |     font-family: 'IBM Plex Mono', monospace;
 84 |     font-size: 11px;
 85 |     color: #8d8d8d;
 86 |     display: flex;
 87 |     gap: 16px;
 88 | }
 89 | .diff-row {
 90 |     display: grid;
 91 |     grid-template-columns: 140px 1fr 1fr 80px 1fr;
 92 |     gap: 0;
 93 |     border-bottom: 1px solid #2a2a2a;
 94 |     font-size: 12px;
 95 |     font-family: 'IBM Plex Mono', monospace;
 96 | }
 97 | .diff-row:last-child { border-bottom: none; }
 98 | .diff-cell { padding: 8px 12px; border-right: 1px solid #2a2a2a; }
 99 | .diff-cell:last-child { border-right: none; }
100 | .diff-label { color: #8d8d8d; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
101 | .diff-legacy { color: #fa4d56; }
102 | .diff-modern { color: #42be65; }
103 | .diff-delta { color: #f1c21b; font-weight: 600; }
104 | 
105 | .live-badge {
106 |     display: inline-block;
107 |     background: #fa4d56;
108 |     color: white;
109 |     font-size: 10px;
110 |     font-family: 'IBM Plex Mono', monospace;
111 |     padding: 2px 8px;
112 |     letter-spacing: 1px;
113 |     animation: pulse 1.5s infinite;
114 | }
115 | @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
116 | 
117 | .ibm-divider { border: none; border-top: 1px solid #393939; margin: 24px 0; }
118 | .bob-panel { background: #1a1a2e; border: 1px solid #0f62fe; border-left: 4px solid #0f62fe; padding: 20px 24px; font-size: 13px; color: #c6c6c6; line-height: 1.6; }
119 | .bob-source-live { background: #042; color: #42be65; font-size: 11px; font-family: 'IBM Plex Mono', monospace; padding: 2px 8px; border: 1px solid #42be65; display: inline-block; margin-bottom: 12px; }
120 | .bob-source-mock { background: #2a2000; color: #f1c21b; font-size: 11px; font-family: 'IBM Plex Mono', monospace; padding: 2px 8px; border: 1px solid #f1c21b; display: inline-block; margin-bottom: 12px; }
121 | 
122 | .stButton > button { background: #0f62fe !important; color: white !important; border: none !important; border-radius: 0 !important; font-family: 'IBM Plex Sans', sans-serif !important; font-size: 14px !important; font-weight: 400 !important; padding: 12px 24px !important; letter-spacing: 0.16px !important; width: 100%; }
123 | .stButton > button:hover { background: #0353e9 !important; }
124 | .stSlider label { color: #c6c6c6 !important; font-size: 13px !important; }
125 | .stSelectbox label { color: #c6c6c6 !important; font-size: 13px !important; }
126 | [data-testid="stMetric"] { background: #262626; border-top: 3px solid #0f62fe; padding: 16px 20px; }
127 | [data-testid="stMetricLabel"] { color: #8d8d8d !important; font-size: 12px !important; }
128 | [data-testid="stMetricValue"] { font-family: 'IBM Plex Mono', monospace !important; color: #f4f4f4 !important; font-size: 28px !important; font-weight: 300 !important; }
129 | .stDataFrame { background: #262626 !important; }
130 | .stDownloadButton > button { background: #42be65 !important; color: #161616 !important; font-weight: 600 !important; }
131 | .stCheckbox label { color: #c6c6c6 !important; font-size: 13px !important; }
132 | 
133 | /* Hero band */
134 | .hero-band { background: linear-gradient(90deg, #161616 0%, #1c1c1c 100%); border-bottom: 1px solid #393939; padding: 28px 32px; margin-bottom: 0; }
135 | .hero-eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #0f62fe; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
136 | .hero-title { font-family: 'IBM Plex Sans', sans-serif; font-size: 36px; font-weight: 300; color: #f4f4f4; line-height: 1.1; margin-bottom: 6px; }
137 | .hero-title b { font-weight: 600; color: #0f62fe; }
138 | .hero-sub { font-family: 'IBM Plex Sans', sans-serif; font-size: 14px; color: #8d8d8d; line-height: 1.5; max-width: 920px; }
139 | 
140 | /* Decision banner */
141 | .decision-banner { padding: 18px 28px; margin: 0; border-left: 6px solid; display: flex; align-items: center; gap: 24px; }
142 | .decision-icon { font-size: 32px; font-family: 'IBM Plex Mono', monospace; font-weight: 600; }
143 | .decision-text-main { font-size: 20px; font-weight: 500; line-height: 1.2; }
144 | .decision-text-sub { font-size: 12px; color: #8d8d8d; font-family: 'IBM Plex Mono', monospace; margin-top: 2px; }
145 | 
146 | /* Phase banners */
147 | .phase-banner { background: #1c1c1c; border-left: 4px solid #0f62fe; padding: 16px 24px; margin: 32px 0 20px 0; display: flex; align-items: center; gap: 18px; }
148 | .phase-num { font-family: 'IBM Plex Mono', monospace; font-size: 28px; font-weight: 300; color: #0f62fe; line-height: 1; min-width: 56px; }
149 | .phase-title { font-size: 18px; font-weight: 500; color: #f4f4f4; line-height: 1.2; }
150 | .phase-desc { font-size: 12px; color: #8d8d8d; margin-top: 4px; line-height: 1.4; }
151 | 
152 | /* Sidebar */
153 | .sb-section { font-family: 'IBM Plex Sans', sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #8d8d8d; padding: 16px 0 8px 0; border-bottom: 1px solid #393939; margin-bottom: 12px; }
154 | .sb-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; font-size: 12px; color: #c6c6c6; }
155 | .sb-row-label { color: #8d8d8d; }
156 | .sb-row-val { font-family: 'IBM Plex Mono', monospace; color: #f4f4f4; }
157 | .sb-status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }
158 | .sb-status-row { display: flex; align-items: center; padding: 5px 0; font-size: 12px; color: #c6c6c6; }
159 | .sb-status-name { flex: 1; }
160 | .sb-status-port { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #6f6f6f; }
161 | .sb-arch-step { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #c6c6c6; padding: 4px 0; border-left: 2px solid #393939; padding-left: 10px; margin-left: 4px; line-height: 1.4; }
162 | .sb-arch-step b { color: #0f62fe; }
163 | 
164 | /* Footer */
165 | .ibm-footer { background: #1c1c1c; border-top: 1px solid #393939; padding: 24px 32px; margin-top: 48px; display: flex; justify-content: space-between; align-items: center; font-family: 'IBM Plex Sans', sans-serif; }
166 | .ibm-footer-left { font-size: 12px; color: #8d8d8d; line-height: 1.5; }
167 | .ibm-footer-right { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #6f6f6f; text-align: right; }
168 | .ibm-footer b { color: #f4f4f4; font-weight: 600; }
169 | </style>
170 | """, unsafe_allow_html=True)
171 | 
172 | # ── Sidebar — System Health & Architecture ────────────────────────────────────
173 | def _check_service(url, timeout=2.0):
174 |     try:
175 |         import httpx
176 |         r = httpx.get(url, timeout=timeout)
177 |         return r.status_code == 200
178 |     except Exception:
179 |         return False
180 | 
181 | def _check_mcp_running():
182 |     try:
183 |         import subprocess
184 |         r = subprocess.run(
185 |             ["wmic", "process", "where", "name='python.exe'", "get", "CommandLine"],
186 |             capture_output=True, text=True, timeout=2.0,
187 |         )
188 |         return "mcp_server.py" in r.stdout
189 |     except Exception:
190 |         return False
191 | 
192 | legacy_up = _check_service("http://localhost:8001/health")
193 | modern_up = _check_service("http://localhost:8002/health")
194 | bob_live  = bool(__import__("os").environ.get("BOB_API_KEY", ""))
195 | mcp_active = _check_mcp_running()
196 | 
197 | with st.sidebar:
198 |     st.markdown("""<div style='padding:8px 0 4px 0;display:flex;align-items:center;gap:10px'>
199 |         <svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#0f62fe' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' style='flex-shrink:0'>
200 |             <path d='m14 13-7.5 7.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L11 10'/>
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
dashboard.py

# VSCode Open Tabs
parity/tenant_config.py,config/tenants.json,parity/parity_engine.py,parity/scoring.py,dashboard.py,parity/confidence.py,parity/drift_detection.py,parity/compliance.py,mcp_server.py,audit/pdf_report.py,ENHANCEMENT_GUIDE.md,tests/test_tenant_config.py,tests/test_confidence.py,tests/test_drift_detection.py,tests/__init__.py,requirements.txt,tests/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-15T18:04:35.936Z
User time zone: Europe/Berlin, UTC+2:00

# Current Cost
$0.08

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>dashboard.py</path>
    <line_range>400-600</line_range>
  </file>
  <file>
    <path>dashboard.py</path>
    <line_range>600-800</line_range>
  </file>
  <file>
    <path>dashboard.py</path>
    <line_range>800-1070</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'dashboard.py', 'dashboard.py', 'dashboard.py'] Result:
<files>
<file><path>dashboard.py</path>
<content lines="400-600">
400 | 
401 |     def _show_scan(pct, msg):
402 |         _scan_ph.markdown(
403 |             f"<div style='background:#161616;border:1px solid #0f62fe;padding:16px 24px;margin:8px 0'>"
404 |             f"<div style='font-family:\"IBM Plex Mono\",monospace;font-size:12px;color:#0f62fe;margin-bottom:10px'>▌ {msg}</div>"
405 |             f"<div style='background:#393939;height:3px'><div style='background:#0f62fe;height:3px;width:{pct}%'></div></div>"
406 |             f"<div style='font-family:\"IBM Plex Mono\",monospace;font-size:10px;color:#6f6f6f;margin-top:6px'>{pct}%</div>"
407 |             f"</div>",
408 |             unsafe_allow_html=True,
409 |         )
410 |         time.sleep(0.35)
411 | 
412 |     _show_scan(20, "Generating transaction sample...")
413 |     _show_scan(45, "Routing through Legacy + Modern banks...")
414 | 
415 |     try:
416 |         pairs = asyncio.run(run_batch(n=n_transactions, demo_mode=demo_mode))
417 |     except Exception as _conn_err:
418 |         _scan_ph.empty()
419 |         st.error(
420 |             "**Banking services offline.** "
421 |             "Start both services before launching the dashboard:\n\n"
422 |             "```\nbash start.sh\n```\n\n"
423 |             f"Detail: `{_conn_err}`"
424 |         )
425 |         st.stop()
426 | 
427 |     # Load tenant profile for analysis
428 |     tenant_id = st.session_state.get("selected_tenant_id", "demo_default")
429 |     tenant = load_tenant(tenant_id)
430 |     
431 |     _show_scan(70, f"Running Parity Engine · {tenant.anomaly_sigma_threshold}σ anomaly detection...")
432 |     results = analyse_batch(pairs, tenant=tenant)
433 |     results = flag_anomalies(results, tenant=tenant)
434 |     _show_scan(92, f"Computing Wilson 95% CI readiness scores (threshold: {tenant.parity_threshold_pct}%)...")
435 |     scores = score_results(results, tenant=tenant)
436 |     _scan_ph.empty()
437 | 
438 |     st.session_state["scores"] = scores
439 |     st.session_state["results"] = results
440 |     st.session_state["current_tenant"] = tenant
441 |     st.session_state["run_ts"] = datetime.now(timezone.utc)
442 |     if "run_history" not in st.session_state:
443 |         st.session_state["run_history"] = []
444 |     entry = {"run": f"Run {len(st.session_state['run_history']) + 1}", "ts": st.session_state["run_ts"].strftime("%H:%M:%S")}
445 |     for s in scores:
446 |         entry[s["function"]] = s["parity_rate_pct"]
447 |     st.session_state["run_history"].append(entry)
448 | 
449 | scores = st.session_state.get("scores", [])
450 | results = st.session_state.get("results", [])
451 | run_ts = st.session_state.get("run_ts", datetime.now(timezone.utc))
452 | 
453 | # ── PDF export ────────────────────────────────────────────────────────────────
454 | if export_pdf and scores:
455 |     bob_resp = st.session_state.get("bob_response") or st.session_state.get("bob_patch_response")
456 |     bob_sid = bob_resp.get("session_id") if bob_resp else None
457 |     
458 |     # Get tenant profile for PDF
459 |     current_tenant = st.session_state.get("current_tenant")
460 |     tenant_profile = current_tenant.to_dict() if current_tenant else None
461 |     
462 |     with st.spinner("Generating audit report..."):
463 |         pdf_bytes = generate_pdf(scores, results, run_ts, bob_session_id=bob_sid, tenant_profile=tenant_profile)
464 |     filename = f"bob_the_judge_audit_{run_ts.strftime('%Y%m%d_%H%M%S')}.pdf"
465 |     st.download_button(
466 |         label="Download Audit Report (PDF)",
467 |         data=pdf_bytes,
468 |         file_name=filename,
469 |         mime="application/pdf",
470 |     )
471 | 
472 | if not scores:
473 |     st.markdown(
474 |         "<div style='margin-top:24px;background:#1c1c1c;border-left:4px solid #0f62fe;"
475 |         "padding:16px 24px;font-family:IBM Plex Mono,monospace;font-size:13px;color:#8d8d8d'>"
476 |         "Enable <b style='color:#c6c6c6'>🎯 Demo</b> for a guaranteed 2-safe / 2-blocked scenario, "
477 |         "then click <b style='color:#c6c6c6'>Run Analysis</b> to start."
478 |         "</div>",
479 |         unsafe_allow_html=True,
480 |     )
481 |     st.stop()
482 | 
483 | # ── KPI row ───────────────────────────────────────────────────────────────────
484 | total_txns = sum(s["total_transactions"] for s in scores)
485 | overall_parity = sum(s["parity_rate_pct"] * s["total_transactions"] for s in scores) / max(total_txns, 1)
486 | safe_functions = sum(1 for s in scores if s["verdict"] == "SAFE_TO_CUT")
487 | do_not_cut = sum(1 for s in scores if s["verdict"] == "DO_NOT_CUT")
488 | total_exposure = sum(
489 |     s.get("exposure_usd", 0) for s in scores
490 |     if s["verdict"] in ("DO_NOT_CUT", "HOLD_INVESTIGATE")
491 | )
492 | anomaly_count = sum(1 for r in results if r.get("anomaly"))
493 | 
494 | # ── Decision Banner (top-line verdict) ────────────────────────────────────────
495 | if do_not_cut == 0 and safe_functions == len(scores):
496 |     db_color, db_bg = "#42be65", "#022b1a"
497 |     db_icon, db_main = "✓", "READY FOR CUTOVER"
498 |     db_sub = f"All {len(scores)} payment functions cleared · zero blockers · zero exposure"
499 | elif do_not_cut == 0:
500 |     db_color, db_bg = "#f1c21b", "#2a1f00"
501 |     db_icon, db_main = "~", "PROCEED WITH MONITORING"
502 |     db_sub = f"{safe_functions} safe · {len(scores)-safe_functions} require monitoring · ${total_exposure:,.0f} exposure"
503 | else:
504 |     db_color, db_bg = "#fa4d56", "#2d0709"
505 |     db_icon, db_main = "✗", "HOLD — DO NOT CUT"
506 |     db_sub = f"{do_not_cut} blocked · {anomaly_count} anomalies (>2σ) · ${total_exposure:,.0f} at risk"
507 | 
508 | st.markdown(f"""
509 | <div class="decision-banner" style="background:{db_bg};border-left-color:{db_color}">
510 |     <div class="decision-icon" style="color:{db_color}">{db_icon}</div>
511 |     <div>
512 |         <div class="decision-text-main" style="color:{db_color}">{db_main}</div>
513 |         <div class="decision-text-sub">{db_sub}</div>
514 |     </div>
515 | </div>
516 | """, unsafe_allow_html=True)
517 | 
518 | # ── PHASE 1 BANNER ────────────────────────────────────────────────────────────
519 | st.markdown("""
520 | <div class="phase-banner">
521 |     <div class="phase-num">01</div>
522 |     <div>
523 |         <div class="phase-title">Live Parity Analysis</div>
524 |         <div class="phase-desc">Routing identical transactions through legacy and modern systems · per-function readiness scoring with 95% confidence intervals</div>
525 |     </div>
526 | </div>
527 | """, unsafe_allow_html=True)
528 | 
529 | st.markdown('<div class="ibm-section-header">System Overview</div>', unsafe_allow_html=True)
530 | 
531 | k1, k2, k3, k4, k5, k6 = st.columns(6)
532 | with k1:
533 |     st.markdown(f"""<div class="kpi-tile">
534 |         <div class="kpi-label">Transactions Analysed</div>
535 |         <div class="kpi-value">{total_txns:,}</div>
536 |         <div class="kpi-sub">This run · {len(scores)} functions</div>
537 |     </div>""", unsafe_allow_html=True)
538 | with k2:
539 |     colour = "#42be65" if overall_parity >= 90 else "#f1c21b" if overall_parity >= 70 else "#fa4d56"
540 |     st.markdown(f"""<div class="kpi-tile" style="border-top-color:{colour}">
541 |         <div class="kpi-label">Overall Parity Rate</div>
542 |         <div class="kpi-value" style="color:{colour}">{overall_parity:.1f}%</div>
543 |         <div class="kpi-sub">Across all payment functions</div>
544 |     </div>""", unsafe_allow_html=True)
545 | with k3:
546 |     st.markdown(f"""<div class="kpi-tile" style="border-top-color:#42be65">
547 |         <div class="kpi-label">Functions Cleared</div>
548 |         <div class="kpi-value" style="color:#42be65">{safe_functions} <span style="font-size:18px;color:#6f6f6f">/ {len(scores)}</span></div>
549 |         <div class="kpi-sub">Safe to cut over now</div>
550 |     </div>""", unsafe_allow_html=True)
551 | with k4:
552 |     c = "#fa4d56" if do_not_cut > 0 else "#42be65"
553 |     st.markdown(f"""<div class="kpi-tile" style="border-top-color:{c}">
554 |         <div class="kpi-label">Functions Blocked</div>
555 |         <div class="kpi-value" style="color:{c}">{do_not_cut}</div>
556 |         <div class="kpi-sub">Require investigation</div>
557 |     </div>""", unsafe_allow_html=True)
558 | with k5:
559 |     exp_colour = "#fa4d56" if total_exposure > 0 else "#42be65"
560 |     exp_str = f"${total_exposure:,.0f}" if total_exposure < 1_000_000 else f"${total_exposure/1_000_000:.1f}M"
561 |     st.markdown(f"""<div class="kpi-tile" style="border-top-color:{exp_colour}">
562 |         <div class="kpi-label">$ Exposure at Risk</div>
563 |         <div class="kpi-value" style="color:{exp_colour}">{exp_str}</div>
564 |         <div class="kpi-sub">In blocked functions (this sample)</div>
565 |     </div>""", unsafe_allow_html=True)
566 | with k6:
567 |     an_colour = "#ff832b" if anomaly_count > 0 else "#42be65"
568 |     st.markdown(f"""<div class="kpi-tile" style="border-top-color:{an_colour}">
569 |         <div class="kpi-label">Anomalies Detected</div>
570 |         <div class="kpi-value" style="color:{an_colour}">{anomaly_count}</div>
571 |         <div class="kpi-sub">Statistically outlying divergences (>2σ)</div>
572 |     </div>""", unsafe_allow_html=True)
573 | 
574 | # ── Function verdict cards ────────────────────────────────────────────────────
575 | st.markdown('<div class="ibm-section-header">Function-Level Cutover Readiness</div>', unsafe_allow_html=True)
576 | 
577 | CARBON_VERDICT = {
578 |     "SAFE_TO_CUT":          {"bg": "#022b1a", "color": "#42be65", "border": "#42be65", "label": "SAFE TO CUT"},
579 |     "CUT_WITH_MONITORING":  {"bg": "#2a1f00", "color": "#f1c21b", "border": "#f1c21b", "label": "CUT WITH MONITORING"},
580 |     "HOLD_INVESTIGATE":     {"bg": "#2a1200", "color": "#ff832b", "border": "#ff832b", "label": "HOLD — INVESTIGATE"},
581 |     "DO_NOT_CUT":           {"bg": "#2d0709", "color": "#fa4d56", "border": "#fa4d56", "label": "DO NOT CUT"},
582 | }
583 | 
584 | cols = st.columns(len(scores))
585 | for col, s in zip(cols, scores):
586 |     v = CARBON_VERDICT.get(s["verdict"], CARBON_VERDICT["DO_NOT_CUT"])
587 |     ci_lo = s.get("ci_low", 0)
588 |     ci_hi = s.get("ci_high", 0)
589 |     exp = s.get("exposure_usd", 0)
590 |     exp_str = f"${exp:,.0f}" if exp < 1_000_000 else f"${exp/1_000_000:.1f}M"
591 |     with col:
592 |         st.markdown(f"""
593 |         <div class="verdict-card">
594 |             <div class="verdict-card-header" style="background:{v['bg']}">
595 |                 <div class="verdict-card-fn">{s['function']}</div>
596 |                 <div class="verdict-card-score" style="color:{v['color']}">{s['readiness_score']:.0f}</div>
597 |                 <div style="font-size:11px;color:#6f6f6f;font-family:'IBM Plex Mono',monospace">/ 100 readiness</div>
598 |             </div>
599 |             <div class="verdict-card-body">
600 |                 <div class="verdict-tag" style="background:{v['bg']};color:{v['color']};border:1px solid {v['border']}">{v['label']}</div>
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
dashboard.py

# VSCode Open Tabs
parity/tenant_config.py,config/tenants.json,parity/parity_engine.py,parity/scoring.py,dashboard.py,parity/confidence.py,parity/drift_detection.py,parity/compliance.py,mcp_server.py,audit/pdf_report.py,ENHANCEMENT_GUIDE.md,tests/test_tenant_config.py,tests/test_confidence.py,tests/test_drift_detection.py,tests/__init__.py,requirements.txt,tests/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-15T18:04:40.438Z
User time zone: Europe/Berlin, UTC+2:00

# Current Cost
$0.21

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Based on my comprehensive code review of the project files, here's a prioritized list of findings:

## 🔴 CRITICAL

1. **SQL Injection Vulnerability in drift_detection.py**
   - **Lines 146-160**: String interpolation in SQL queries with `f-string` for column names
   - **Risk**: While `function_name` and `tenant_id` come from internal sources, this pattern is dangerous
   - **Impact**: Could allow SQL injection if user input ever reaches these parameters
   - **Fix**: Use parameterized queries or whitelist validation

2. **Missing Database Connection Cleanup**
   - **drift_detection.py lines 104-128, 143-163**: SQLite connections not using context managers
   - **Risk**: Connection leaks under exceptions, file locks on Windows
   - **Impact**: Database corruption, resource exhaustion in production
   - **Railway Risk**: Container restart issues with locked DB files

3. **Unhandled Division by Zero**
   - **dashboard.py line 485**: `max(total_txns, 1)` protects but inconsistent
   - **confidence.py line 306**: `(successes / trials * 100)` unprotected
   - **Risk**: Runtime crash if `trials=0` slips through
   - **Impact**: Dashboard crash, MCP server failure

## 🟠 HIGH

4. **Missing Error Handling in MCP Server**
   - **mcp_server.py lines 49-58**: No try-catch around `run_batch()` or `load_tenant()`
   - **Risk**: Unhandled exceptions crash entire MCP server
   - **Impact**: Bob IDE loses connection, requires manual restart
   - **Railway Risk**: Container crash loop

5. **Hardcoded Mock Data in Production Code**
   - **mcp_server.py lines 505-522**: Mock scores in `assess_compliance()`
   - **Risk**: Compliance assessment returns fake data instead of real analysis
   - **Regulator Risk**: FALSE compliance attestation could be generated
   - **Impact**: Legal liability, audit failure

6. **Race Condition in Session State**
   - **dashboard.py lines 438-447**: Multiple writes to `st.session_state` without locks
   - **Risk**: Concurrent analysis runs could corrupt state
   - **Impact**: Wrong tenant profile applied, incorrect verdicts

7. **Missing Input Validation**
   - **tenant_config.py lines 100-113**: No validation of JSON data types
   - **Risk**: Malformed `tenants.json` causes runtime errors
   - **Impact**: Application crash on startup
   - **Example**: `Decimal(str(data["fee_tolerance_usd"]))` fails if value is already Decimal or invalid

8. **Unsafe File Path Construction**
   - **drift_detection.py line 57**: `Path(db_path)` with user input
   - **tenant_config.py line 81**: Relative path construction
   - **Risk**: Path traversal if `db_path` comes from external source
   - **Impact**: Write to arbitrary filesystem locations

## 🟡 MEDIUM

9. **Missing Drift Detection Integration**
   - **dashboard.py**: Drift detection module exists but never called in UI
   - **Risk**: Parity degradation goes undetected over time
   - **Impact**: False confidence in cutover readiness

10. **Bootstrap Random Seed Fixed**
    - **confidence.py line 97**: `rng = np.random.default_rng(42)`
    - **Risk**: Bootstrap intervals always identical, defeats purpose
    - **Impact**: No true uncertainty quantification

11. **PDF Generation Memory Issues**
    - **audit/pdf_report.py line 259**: Loads all divergent transactions into memory
    - **Risk**: OOM with large datasets (>10K divergences)
    - **Railway Risk**: Container OOM kill

12. **Missing Timeout on HTTP Checks**
    - **dashboard.py line 176**: `timeout=2.0` but no retry logic
    - **Risk**: False negatives on slow network
    - **Impact**: Shows services as down when they're just slow

13. **Compliance Assessment Not Persisted**
    - **compliance.py**: Assessments generated but not stored
    - **Risk**: No audit trail of compliance decisions
    - **Regulator Risk**: Cannot prove compliance at specific timestamp

## 🟢 LOW

14. **Inconsistent Error Messages**
    - Various files use different error message formats
    - **Impact**: Poor user experience, harder debugging

15. **Missing Type Hints**
    - **dashboard.py**: Most functions lack type hints
    - **Impact**: Harder maintenance, no IDE autocomplete

16. **Hardcoded Port Numbers**
    - **dashboard.py lines 192-193**: `8001`, `8002` hardcoded
    - **Risk**: Conflicts in multi-tenant deployments
    - **Impact**: Cannot run multiple instances

17. **No Logging Framework**
    - All modules lack structured logging
    - **Risk**: Cannot debug production issues
    - **Railway Risk**: No CloudWatch/logging integration

18. **Missing Test Coverage**
    - **drift_detection.py**: No tests for CUSUM/EWMA algorithms
    - **compliance.py**: No tests for regulatory assessments
    - **mcp_server.py**: No integration tests
    - **Risk**: Regressions go undetected

19. **Dashboard Performance**
    - **dashboard.py lines 752-850**: Rebuilds entire history chart on every render
    - **Risk**: Slow UI with >50 runs in history
    - **Impact**: Poor user experience

20. **Missing Configuration Validation**
    - **tenants.json**: No JSON schema validation
    - **Risk**: Typos cause runtime errors
    - **Impact**: Application fails to start

---

## 🎯 **Top 3 Must-Fix Before Production:**

1. **SQL Injection + Connection Leaks** (drift_detection.py) - Could corrupt audit trail
2. **Mock Data in Compliance** (mcp_server.py) - Legal/regulatory liability
3. **Missing Error Handling in MCP** - Crashes entire Bob integration

## 🚂 **Railway Deployment Risks:**

- Database file locking on container restart (SQLite)
- No health check endpoints for Railway
- Missing environment variable validation
- No graceful shutdown handling
- Memory leaks from unclosed connections

## 📋 **Regulator Concerns:**

- Compliance attestations based on mock data
- No audit trail persistence
- Missing drift detection in production flow
- Hardcoded thresholds not tenant-specific in some paths
- PDF reports don't include data lineage/provenance

---

**User:**

[ERROR] You did not use a tool in your previous response! Please retry with a tool use.

# Reminder: Instructions for Tool Use

Tool uses are formatted using XML-style tags. The tool name itself becomes the XML tag name. Each parameter is enclosed within its own set of tags. Here's the structure:

<actual_tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</actual_tool_name>

For example, to use the attempt_completion tool:

<attempt_completion>
<result>
I have completed the task...
</result>
</attempt_completion>

Always use the actual tool name as the XML tag name for proper parsing and execution.

# Next Steps

If you have completed the user's task, use the attempt_completion tool.
If you require additional information from the user, use the ask_followup_question tool.
Otherwise, if you have not completed the task and do not need additional information, then proceed with the next step of the task.
(This is an automated message, so do not respond to it conversationally.)
<environment_details>
# VSCode Visible Files
dashboard.py

# VSCode Open Tabs
parity/tenant_config.py,config/tenants.json,parity/parity_engine.py,parity/scoring.py,dashboard.py,parity/confidence.py,parity/drift_detection.py,parity/compliance.py,mcp_server.py,audit/pdf_report.py,ENHANCEMENT_GUIDE.md,tests/test_tenant_config.py,tests/test_confidence.py,tests/test_drift_detection.py,tests/__init__.py,requirements.txt,tests/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-15T18:05:14.941Z
User time zone: Europe/Berlin, UTC+2:00

# Current Cost
$0.36

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
# Code Review: Bob the Judge - Prioritized Findings

## 🔴 CRITICAL

1. **SQL Injection Vulnerability** ([`drift_detection.py:146-160`](parity/drift_detection.py:146))
   - String interpolation in SQL queries using f-strings for column names
   - While inputs are currently internal, pattern is dangerous for future changes
   - **Fix**: Use parameterized queries or whitelist validation

2. **Database Connection Leaks** ([`drift_detection.py:104-128`](parity/drift_detection.py:104), [`143-163`](parity/drift_detection.py:143))
   - SQLite connections not using context managers
   - **Railway Risk**: File locks on Windows, corruption on container restart
   - **Fix**: Use `with sqlite3.connect()` pattern

3. **Division by Zero** ([`confidence.py:306`](parity/confidence.py:306))
   - Unprotected division: `(successes / trials * 100)` when `trials=0`
   - **Impact**: MCP server crash, dashboard failure
   - **Fix**: Add zero check before division

## 🟠 HIGH

4. **MCP Server Missing Error Handling** ([`mcp_server.py:49-58`](mcp_server.py:49))
   - No try-catch around [`run_batch()`](mcp_server.py:55), [`load_tenant()`](mcp_server.py:54)
   - **Impact**: Entire MCP server crashes, Bob IDE loses connection
   - **Railway Risk**: Container crash loop

5. **Mock Data in Production Compliance** ([`mcp_server.py:505-522`](mcp_server.py:505))
   - [`assess_compliance()`](mcp_server.py:484) returns hardcoded mock scores
   - **Regulator Risk**: FALSE compliance attestations could be generated
   - **Impact**: Legal liability, audit failure

6. **Race Condition in Session State** ([`dashboard.py:438-447`](dashboard.py:438))
   - Multiple writes to `st.session_state` without synchronization
   - **Impact**: Wrong tenant profile applied, incorrect verdicts

7. **Missing Input Validation** ([`tenant_config.py:100-113`](parity/tenant_config.py:100))
   - No validation of JSON data types from [`tenants.json`](config/tenants.json)
   - [`Decimal(str(data["fee_tolerance_usd"]))`](parity/tenant_config.py:104) fails on invalid input
   - **Impact**: Application crash on startup

8. **Unsafe File Path Construction** ([`drift_detection.py:57`](parity/drift_detection.py:57))
   - `Path(db_path)` with user-controllable input
   - **Risk**: Path traversal vulnerability

## 🟡 MEDIUM

9. **Drift Detection Not Integrated** ([`dashboard.py`](dashboard.py:1))
   - [`DriftDetector`](parity/drift_detection.py:43) module exists but never called in UI
   - **Impact**: Parity degradation goes undetected over time

10. **Fixed Bootstrap Seed** ([`confidence.py:97`](parity/confidence.py:97))
    - `rng = np.random.default_rng(42)` defeats bootstrap purpose
    - **Impact**: No true uncertainty quantification

11. **PDF Memory Issues** ([`audit/pdf_report.py:259`](audit/pdf_report.py:259))
    - Loads all divergent transactions into memory
    - **Railway Risk**: OOM with >10K divergences

12. **No HTTP Retry Logic** ([`dashboard.py:176`](dashboard.py:176))
    - Single timeout check, no retries
    - **Impact**: False negatives on slow networks

13. **Compliance Not Persisted** ([`compliance.py`](parity/compliance.py:1))
    - Assessments generated but not stored
    - **Regulator Risk**: No audit trail at specific timestamps

## 🟢 LOW

14. **Missing Type Hints** ([`dashboard.py`](dashboard.py:1))
    - Most functions lack type annotations

15. **Hardcoded Ports** ([`dashboard.py:192-193`](dashboard.py:192))
    - Cannot run multiple instances

16. **No Structured Logging**
    - Cannot debug production issues on Railway

17. **Missing Test Coverage**
    - [`drift_detection.py`](parity/drift_detection.py:1), [`compliance.py`](parity/compliance.py:1), [`mcp_server.py`](mcp_server.py:1) lack tests

18. **Dashboard Performance** ([`dashboard.py:752-850`](dashboard.py:752))
    - Rebuilds entire history chart on every render

19. **No Config Validation**
    - [`tenants.json`](config/tenants.json) has no JSON schema

## 🎯 Top 3 Must-Fix Before Production

1. **SQL Injection + Connection Leaks** - Could corrupt audit trail
2. **Mock Data in Compliance** - Legal/regulatory liability  
3. **MCP Error Handling** - Crashes entire Bob integration

## 🚂 Railway Deployment Risks

- SQLite file locking on container restart
- No health check endpoints
- Missing environment variable validation
- No graceful shutdown handling
- Memory leaks from unclosed connections

## 📋 Regulator Concerns

- Compliance attestations based on mock data
- No audit trail persistence
- Drift detection not in production flow
- PDF reports lack data lineage/provenance
</result>
</attempt_completion>

