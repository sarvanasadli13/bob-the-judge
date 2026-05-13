import asyncio
import time
from datetime import datetime, timezone
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from parity.traffic_generator import run_batch
from parity.parity_engine import analyse_batch, flag_anomalies
from parity.scoring import score_results
from audit.pdf_report import generate_pdf
from bob.client import ask_bob

st.set_page_config(
    page_title="Bob the Judge — IBM Migration Advisor",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── IBM Carbon Design System CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif;
}

.stApp { background-color: #161616; }
section[data-testid="stSidebar"] { background-color: #262626; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

.ibm-topbar {
    background: #0f62fe;
    padding: 0 32px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.ibm-topbar-left { display: flex; align-items: center; gap: 16px; }
.ibm-logo { font-family: 'IBM Plex Sans', sans-serif; font-weight: 600; font-size: 18px; color: white; letter-spacing: 2px; }
.ibm-product-name { font-family: 'IBM Plex Sans', sans-serif; font-size: 14px; color: rgba(255,255,255,0.75); border-left: 1px solid rgba(255,255,255,0.3); padding-left: 16px; }
.ibm-topbar-right { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: rgba(255,255,255,0.6); }

.ibm-section-header {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
    color: #8d8d8d; padding: 24px 0 8px 0; border-bottom: 1px solid #393939; margin-bottom: 16px;
}

.kpi-tile { background: #262626; border-top: 3px solid #0f62fe; padding: 20px 24px; min-height: 96px; }
.kpi-label { font-size: 12px; color: #8d8d8d; font-weight: 400; margin-bottom: 6px; letter-spacing: 0.16px; }
.kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 32px; font-weight: 300; color: #f4f4f4; line-height: 1; }
.kpi-sub { font-size: 11px; color: #6f6f6f; margin-top: 4px; }

.verdict-card { background: #262626; border: 1px solid #393939; padding: 0; overflow: hidden; }
.verdict-card-header { padding: 12px 16px; border-bottom: 1px solid #393939; }
.verdict-card-fn { font-size: 11px; color: #8d8d8d; font-weight: 500; letter-spacing: 0.32px; text-transform: uppercase; margin-bottom: 2px; }
.verdict-card-score { font-family: 'IBM Plex Mono', monospace; font-size: 48px; font-weight: 300; line-height: 1; }
.verdict-card-body { padding: 12px 16px; }
.verdict-tag { display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: 0.16px; padding: 2px 8px; margin-bottom: 10px; }
.verdict-stat { font-size: 12px; color: #c6c6c6; line-height: 1.8; font-family: 'IBM Plex Sans', sans-serif; }
.verdict-stat span { font-family: 'IBM Plex Mono', monospace; color: #f4f4f4; }
.ci-band { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #6f6f6f; margin-top: 6px; border-top: 1px solid #393939; padding-top: 6px; }

.diff-card {
    background: #1c1c1c;
    border: 1px solid #393939;
    margin-bottom: 12px;
    overflow: hidden;
}
.diff-card-header {
    background: #262626;
    padding: 8px 16px;
    border-bottom: 1px solid #393939;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #8d8d8d;
    display: flex;
    gap: 16px;
}
.diff-row {
    display: grid;
    grid-template-columns: 140px 1fr 1fr 80px 1fr;
    gap: 0;
    border-bottom: 1px solid #2a2a2a;
    font-size: 12px;
    font-family: 'IBM Plex Mono', monospace;
}
.diff-row:last-child { border-bottom: none; }
.diff-cell { padding: 8px 12px; border-right: 1px solid #2a2a2a; }
.diff-cell:last-child { border-right: none; }
.diff-label { color: #8d8d8d; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
.diff-legacy { color: #fa4d56; }
.diff-modern { color: #42be65; }
.diff-delta { color: #f1c21b; font-weight: 600; }

.live-badge {
    display: inline-block;
    background: #fa4d56;
    color: white;
    font-size: 10px;
    font-family: 'IBM Plex Mono', monospace;
    padding: 2px 8px;
    letter-spacing: 1px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }

.ibm-divider { border: none; border-top: 1px solid #393939; margin: 24px 0; }
.bob-panel { background: #1a1a2e; border: 1px solid #0f62fe; border-left: 4px solid #0f62fe; padding: 20px 24px; font-size: 13px; color: #c6c6c6; line-height: 1.6; }
.bob-source-live { background: #042; color: #42be65; font-size: 11px; font-family: 'IBM Plex Mono', monospace; padding: 2px 8px; border: 1px solid #42be65; display: inline-block; margin-bottom: 12px; }
.bob-source-mock { background: #2a2000; color: #f1c21b; font-size: 11px; font-family: 'IBM Plex Mono', monospace; padding: 2px 8px; border: 1px solid #f1c21b; display: inline-block; margin-bottom: 12px; }

.stButton > button { background: #0f62fe !important; color: white !important; border: none !important; border-radius: 0 !important; font-family: 'IBM Plex Sans', sans-serif !important; font-size: 14px !important; font-weight: 400 !important; padding: 12px 24px !important; letter-spacing: 0.16px !important; width: 100%; }
.stButton > button:hover { background: #0353e9 !important; }
.stSlider label { color: #c6c6c6 !important; font-size: 13px !important; }
.stSelectbox label { color: #c6c6c6 !important; font-size: 13px !important; }
[data-testid="stMetric"] { background: #262626; border-top: 3px solid #0f62fe; padding: 16px 20px; }
[data-testid="stMetricLabel"] { color: #8d8d8d !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { font-family: 'IBM Plex Mono', monospace !important; color: #f4f4f4 !important; font-size: 28px !important; font-weight: 300 !important; }
.stDataFrame { background: #262626 !important; }
.stDownloadButton > button { background: #42be65 !important; color: #161616 !important; font-weight: 600 !important; }
.stCheckbox label { color: #c6c6c6 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
st.markdown(f"""
<div class="ibm-topbar">
    <div class="ibm-topbar-left">
        <span class="ibm-logo">IBM</span>
        <span class="ibm-product-name">⚖ Bob the Judge &nbsp;·&nbsp; Migration Cutover Advisor</span>
    </div>
    <div class="ibm-topbar-right">{now_str} &nbsp;|&nbsp; <span style="color:#42be65">⬤</span> MCP READY</div>
</div>
""", unsafe_allow_html=True)

# ── Controls bar ──────────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([3, 1, 1, 1, 1])
with ctrl1:
    n_transactions = st.slider("Transaction sample size", 20, 300, 80, step=10)
with ctrl2:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
    run_analysis = st.button("Run Analysis")
with ctrl3:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
    export_pdf = st.button("Export PDF")
with ctrl4:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
    live_mode = st.checkbox("🔴 Live")
with ctrl5:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
    demo_mode = st.checkbox("🎯 Demo", help="Fixed scenario — guarantees 2 safe + 2 blocked for consistent demos")

# ── Run analysis ──────────────────────────────────────────────────────────────
if run_analysis:
    with st.spinner("Routing traffic through legacy and modern systems..."):
        try:
            pairs = asyncio.run(run_batch(n=n_transactions, demo_mode=demo_mode))
        except Exception as _conn_err:
            st.error(
                "**Banking services offline.** "
                "Start both services before launching the dashboard:\n\n"
                "```\nbash start.sh\n```\n\n"
                f"Detail: `{_conn_err}`"
            )
            st.stop()
        results = analyse_batch(pairs)
        results = flag_anomalies(results)
        scores = score_results(results)
        st.session_state["scores"] = scores
        st.session_state["results"] = results
        st.session_state["run_ts"] = datetime.now(timezone.utc)
        if "run_history" not in st.session_state:
            st.session_state["run_history"] = []
        entry = {"run": f"Run {len(st.session_state['run_history']) + 1}", "ts": st.session_state["run_ts"].strftime("%H:%M:%S")}
        for s in scores:
            entry[s["function"]] = s["parity_rate_pct"]
        st.session_state["run_history"].append(entry)

scores = st.session_state.get("scores", [])
results = st.session_state.get("results", [])
run_ts = st.session_state.get("run_ts", datetime.now(timezone.utc))

# ── PDF export ────────────────────────────────────────────────────────────────
if export_pdf and scores:
    with st.spinner("Generating audit report..."):
        pdf_bytes = generate_pdf(scores, results, run_ts)
    filename = f"bob_the_judge_audit_{run_ts.strftime('%Y%m%d_%H%M%S')}.pdf"
    st.download_button(
        label="Download Audit Report (PDF)",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
    )

if not scores:
    st.markdown("""
    <div style='background:#1a1a2e;border:1px solid #0f62fe;border-left:4px solid #0f62fe;padding:28px 32px;margin:24px 0'>
        <div style='font-family:IBM Plex Sans,sans-serif;font-size:22px;font-weight:600;color:#f4f4f4;margin-bottom:10px'>
            When is it safe to flip the switch?
        </div>
        <div style='font-family:IBM Plex Sans,sans-serif;font-size:14px;color:#c6c6c6;line-height:1.7;max-width:720px'>
            Bob the Judge runs live payment transactions through your legacy and modern banking systems simultaneously,
            scores parity at function level, and tells you exactly which functions are safe to cut over today —
            with a regulator-grade audit trail in one click.
        </div>
        <div style='margin-top:18px;font-family:IBM Plex Mono,monospace;font-size:12px;color:#6f6f6f'>
            → Enable <b style='color:#c6c6c6'>Demo Mode</b> above for a consistent guided scenario &nbsp;·&nbsp;
            Click <b style='color:#c6c6c6'>Run Analysis</b> to start
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── KPI row ───────────────────────────────────────────────────────────────────
total_txns = sum(s["total_transactions"] for s in scores)
overall_parity = sum(s["parity_rate_pct"] * s["total_transactions"] for s in scores) / max(total_txns, 1)
safe_functions = sum(1 for s in scores if s["verdict"] == "SAFE_TO_CUT")
do_not_cut = sum(1 for s in scores if s["verdict"] == "DO_NOT_CUT")
total_exposure = sum(
    s.get("exposure_usd", 0) for s in scores
    if s["verdict"] in ("DO_NOT_CUT", "HOLD_INVESTIGATE")
)
anomaly_count = sum(1 for r in results if r.get("anomaly"))

st.markdown('<div class="ibm-section-header">System Overview</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.markdown(f"""<div class="kpi-tile">
        <div class="kpi-label">Transactions Analysed</div>
        <div class="kpi-value">{total_txns:,}</div>
        <div class="kpi-sub">This run · {len(scores)} functions</div>
    </div>""", unsafe_allow_html=True)
with k2:
    colour = "#42be65" if overall_parity >= 90 else "#f1c21b" if overall_parity >= 70 else "#fa4d56"
    st.markdown(f"""<div class="kpi-tile" style="border-top-color:{colour}">
        <div class="kpi-label">Overall Parity Rate</div>
        <div class="kpi-value" style="color:{colour}">{overall_parity:.1f}%</div>
        <div class="kpi-sub">Across all payment functions</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-tile" style="border-top-color:#42be65">
        <div class="kpi-label">Functions Cleared</div>
        <div class="kpi-value" style="color:#42be65">{safe_functions} <span style="font-size:18px;color:#6f6f6f">/ {len(scores)}</span></div>
        <div class="kpi-sub">Safe to cut over now</div>
    </div>""", unsafe_allow_html=True)
with k4:
    c = "#fa4d56" if do_not_cut > 0 else "#42be65"
    st.markdown(f"""<div class="kpi-tile" style="border-top-color:{c}">
        <div class="kpi-label">Functions Blocked</div>
        <div class="kpi-value" style="color:{c}">{do_not_cut}</div>
        <div class="kpi-sub">Require investigation</div>
    </div>""", unsafe_allow_html=True)
with k5:
    exp_colour = "#fa4d56" if total_exposure > 0 else "#42be65"
    exp_str = f"${total_exposure:,.0f}" if total_exposure < 1_000_000 else f"${total_exposure/1_000_000:.1f}M"
    st.markdown(f"""<div class="kpi-tile" style="border-top-color:{exp_colour}">
        <div class="kpi-label">$ Exposure at Risk</div>
        <div class="kpi-value" style="color:{exp_colour}">{exp_str}</div>
        <div class="kpi-sub">In blocked functions (this sample)</div>
    </div>""", unsafe_allow_html=True)
with k6:
    an_colour = "#ff832b" if anomaly_count > 0 else "#42be65"
    st.markdown(f"""<div class="kpi-tile" style="border-top-color:{an_colour}">
        <div class="kpi-label">Anomalies Detected</div>
        <div class="kpi-value" style="color:{an_colour}">{anomaly_count}</div>
        <div class="kpi-sub">Statistically outlying divergences (>2σ)</div>
    </div>""", unsafe_allow_html=True)

# ── Function verdict cards ────────────────────────────────────────────────────
st.markdown('<div class="ibm-section-header">Function-Level Cutover Readiness</div>', unsafe_allow_html=True)

CARBON_VERDICT = {
    "SAFE_TO_CUT":          {"bg": "#022b1a", "color": "#42be65", "border": "#42be65", "label": "SAFE TO CUT"},
    "CUT_WITH_MONITORING":  {"bg": "#2a1f00", "color": "#f1c21b", "border": "#f1c21b", "label": "CUT WITH MONITORING"},
    "HOLD_INVESTIGATE":     {"bg": "#2a1200", "color": "#ff832b", "border": "#ff832b", "label": "HOLD — INVESTIGATE"},
    "DO_NOT_CUT":           {"bg": "#2d0709", "color": "#fa4d56", "border": "#fa4d56", "label": "DO NOT CUT"},
}

cols = st.columns(len(scores))
for col, s in zip(cols, scores):
    v = CARBON_VERDICT.get(s["verdict"], CARBON_VERDICT["DO_NOT_CUT"])
    ci_lo = s.get("ci_low", 0)
    ci_hi = s.get("ci_high", 0)
    exp = s.get("exposure_usd", 0)
    exp_str = f"${exp:,.0f}" if exp < 1_000_000 else f"${exp/1_000_000:.1f}M"
    with col:
        st.markdown(f"""
        <div class="verdict-card">
            <div class="verdict-card-header" style="background:{v['bg']}">
                <div class="verdict-card-fn">{s['function']}</div>
                <div class="verdict-card-score" style="color:{v['color']}">{s['readiness_score']:.0f}</div>
                <div style="font-size:11px;color:#6f6f6f;font-family:'IBM Plex Mono',monospace">/ 100 readiness</div>
            </div>
            <div class="verdict-card-body">
                <div class="verdict-tag" style="background:{v['bg']};color:{v['color']};border:1px solid {v['border']}">{v['label']}</div>
                <div class="verdict-stat">
                    Parity rate &nbsp;<span>{s['parity_rate_pct']:.1f}%</span><br>
                    Transactions &nbsp;<span>{s['total_transactions']}</span><br>
                    Avg fee delta &nbsp;<span>${s['avg_fee_diff_usd']:.4f}</span><br>
                    Latency gain &nbsp;<span>{s['avg_latency_improvement_pct']:+.1f}%</span><br>
                    Exposure &nbsp;<span style="color:{'#fa4d56' if exp > 0 else '#42be65'}">{exp_str}</span>
                </div>
                <div class="ci-band">95% CI &nbsp; {ci_lo:.1f}% – {ci_hi:.1f}% &nbsp;(n={s['total_transactions']})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Bob's Live Patch (the demo's wow moment) ──────────────────────────────────
patch_active = st.session_state.get("patch_applied", False)
show_patch_section = (do_not_cut > 0) or patch_active

if show_patch_section:
    st.markdown('<div class="ibm-section-header">Bob\'s Live Patch</div>', unsafe_allow_html=True)

    if not patch_active:
        pcol1, pcol2 = st.columns([1, 3])
        with pcol1:
            apply_patch_btn = st.button("Apply Bob's Patch & Re-Analyse", key="apply_patch")
        with pcol2:
            st.markdown(
                "<div style='color:#c6c6c6;font-size:13px;padding-top:8px;line-height:1.5'>"
                "Bob detected divergences in <b>International</b> and <b>High-Value Wire Transfer</b>. "
                "Click to deploy Bob's parallel-run compatibility patch — modern systems align with "
                "legacy fee logic during dual-run, then switch back after cutover completes."
                "</div>",
                unsafe_allow_html=True,
            )

        if apply_patch_btn:
            with st.spinner("Bob is generating and deploying the patch..."):
                # Get Bob's code response describing the patch
                bob_patch = ask_bob(
                    "code",
                    "Generate compatibility patch to align modern fee logic with legacy during parallel run.",
                    {"scores": scores, "total_txns": total_txns, "overall_parity": round(overall_parity, 1)},
                )
                st.session_state["bob_patch_response"] = bob_patch

                # Apply the patch via admin endpoint
                import httpx
                try:
                    httpx.post("http://localhost:8002/admin/apply_patch", json={}, timeout=5.0)
                except Exception as e:
                    st.error(f"Patch deployment failed: {e}")
                    st.stop()

                # Re-run analysis to show flipped verdict
                pairs_new = asyncio.run(run_batch(n=n_transactions))
                results_new = analyse_batch(pairs_new)
                results_new = flag_anomalies(results_new)
                scores_new = score_results(results_new)
                st.session_state["scores"] = scores_new
                st.session_state["results"] = results_new
                st.session_state["run_ts"] = datetime.now(timezone.utc)

                if "run_history" not in st.session_state:
                    st.session_state["run_history"] = []
                entry = {
                    "run": f"Run {len(st.session_state['run_history']) + 1} (post-patch)",
                    "ts": st.session_state["run_ts"].strftime("%H:%M:%S"),
                }
                for s in scores_new:
                    entry[s["function"]] = s["parity_rate_pct"]
                st.session_state["run_history"].append(entry)
                st.session_state["patch_applied"] = True
            st.rerun()

    else:
        # Patch is active — show status and reset option
        st.markdown(
            "<div style='background:#022b1a;border:1px solid #42be65;padding:14px 18px;margin-bottom:14px'>"
            "<span style='color:#42be65;font-weight:600;font-size:14px'>✓ BOB'S PATCH DEPLOYED</span>&nbsp;&nbsp;"
            "<span style='color:#c6c6c6;font-size:13px'>"
            "Modern banking system aligned with legacy fee logic during parallel run. "
            "Verdicts flipped — see updated scorecards above."
            "</span></div>",
            unsafe_allow_html=True,
        )

        rcol1, rcol2 = st.columns([1, 3])
        with rcol1:
            reset_btn = st.button("Reset Patch (restore original)", key="reset_patch")
        with rcol2:
            st.markdown(
                "<div style='color:#8d8d8d;font-size:12px;padding-top:8px'>"
                "Resetting will restore the original modern fee logic and re-run analysis."
                "</div>",
                unsafe_allow_html=True,
            )

        if reset_btn:
            import httpx
            try:
                httpx.post("http://localhost:8002/admin/reset_patches", json={}, timeout=5.0)
            except Exception:
                pass
            pairs_new = asyncio.run(run_batch(n=n_transactions))
            results_new = analyse_batch(pairs_new)
            results_new = flag_anomalies(results_new)
            scores_new = score_results(results_new)
            st.session_state["scores"] = scores_new
            st.session_state["results"] = results_new
            st.session_state["run_ts"] = datetime.now(timezone.utc)
            st.session_state["patch_applied"] = False
            st.session_state.pop("bob_patch_response", None)
            st.rerun()

        # Show Bob's patch code (so judges see what was deployed)
        if "bob_patch_response" in st.session_state:
            resp = st.session_state["bob_patch_response"]
            st.markdown(
                "<div class='bob-panel'>"
                "<div class='bob-source-mock'>○ IBM Bob API — connecting at hackathon kickoff</div>"
                f"&nbsp;·&nbsp;<span style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#6f6f6f'>"
                f"mode:code &nbsp; session:{resp['session_id']}</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(resp["content"])

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="ibm-section-header">Analysis Charts</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

IBM_CHART_THEME = dict(
    template="plotly_dark",
    plot_bgcolor="#262626",
    paper_bgcolor="#161616",
    font=dict(family="IBM Plex Sans, sans-serif", color="#c6c6c6", size=12),
    margin=dict(l=20, r=20, t=36, b=20),
)

with ch1:
    st.markdown("<div style='color:#8d8d8d;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>Parity Rate by Function — with 95% CI</div>", unsafe_allow_html=True)
    df = pd.DataFrame(scores)
    fig = go.Figure()
    color_map = {"SAFE_TO_CUT": "#42be65", "CUT_WITH_MONITORING": "#f1c21b", "HOLD_INVESTIGATE": "#ff832b", "DO_NOT_CUT": "#fa4d56"}
    for _, row in df.iterrows():
        bar_color = color_map.get(row["verdict"], "#8d8d8d")
        ci_lo = row.get("ci_low", row["parity_rate_pct"])
        ci_hi = row.get("ci_high", row["parity_rate_pct"])
        fig.add_trace(go.Bar(
            x=[row["function"]], y=[row["parity_rate_pct"]],
            marker_color=bar_color, name=row["verdict"], showlegend=False,
            error_y=dict(
                type="data", symmetric=False,
                array=[ci_hi - row["parity_rate_pct"]],
                arrayminus=[row["parity_rate_pct"] - ci_lo],
                color="#8d8d8d", thickness=1.5, width=6,
            ),
        ))
    fig.add_hline(y=95, line_dash="dot", line_color="#0f62fe", line_width=1.5,
                  annotation_text="Cut threshold 95%", annotation_font_color="#0f62fe", annotation_font_size=11)
    fig.update_layout(showlegend=False, yaxis=dict(range=[0, 110], gridcolor="#393939"), xaxis=dict(gridcolor="#393939"), **IBM_CHART_THEME)
    st.plotly_chart(fig, use_container_width=True)

with ch2:
    st.markdown("<div style='color:#8d8d8d;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>Processing Latency: Legacy vs Modern</div>", unsafe_allow_html=True)
    if results:
        df_r = pd.DataFrame(results)
        fig2 = go.Figure()
        fig2.add_trace(go.Box(
            y=df_r["legacy_latency_ms"], name="Legacy (COBOL)",
            marker_color="#fa4d56", line_color="#fa4d56", fillcolor="rgba(250,77,86,0.15)", boxmean=True,
        ))
        fig2.add_trace(go.Box(
            y=df_r["modern_latency_ms"], name="Modern",
            marker_color="#42be65", line_color="#42be65", fillcolor="rgba(66,190,101,0.15)", boxmean=True,
        ))
        fig2.update_layout(yaxis=dict(title="ms", gridcolor="#393939"), xaxis=dict(gridcolor="#393939"), **IBM_CHART_THEME)
        st.plotly_chart(fig2, use_container_width=True)

# ── Parity trend history ──────────────────────────────────────────────────────
history = st.session_state.get("run_history", [])
if len(history) > 1:
    st.markdown('<div class="ibm-section-header">Parity Trend — Run History</div>', unsafe_allow_html=True)
    df_hist = pd.DataFrame(history)
    fn_colors = {
        "Domestic Wire Transfer":       "#42be65",
        "Scheduled Payment":            "#42be65",
        "International Wire Transfer":  "#fa4d56",
        "High-Value Wire Transfer":     "#fa4d56",
    }
    fig_hist = go.Figure()
    for fn in [c for c in df_hist.columns if c not in ("run", "ts")]:
        color = fn_colors.get(fn, "#8d8d8d")
        fig_hist.add_trace(go.Scatter(
            x=df_hist["run"], y=df_hist[fn],
            name=fn, mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=7, symbol="circle"),
        ))
    fig_hist.add_hline(y=95, line_dash="dot", line_color="#0f62fe", line_width=1.5,
                       annotation_text="Cut threshold 95%", annotation_font_color="#0f62fe", annotation_font_size=11)
    fig_hist.update_layout(
        yaxis=dict(range=[0, 108], title="Parity %", gridcolor="#393939"),
        xaxis=dict(gridcolor="#393939"),
        legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        **IBM_CHART_THEME,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ── Side-by-side divergence diff ──────────────────────────────────────────────
divergent = [r for r in results if not r["parity"]]
if divergent:
    st.markdown('<div class="ibm-section-header">Divergence Deep Dive — Field-Level Diff</div>', unsafe_allow_html=True)

    worst = sorted(divergent, key=lambda r: sum(
        3 if d["severity"] == "CRITICAL" else 2 if d["severity"] == "HIGH" else 1
        for d in r["divergences"]
    ), reverse=True)[:6]

    sev_colors = {"CRITICAL": "#fa4d56", "HIGH": "#ff832b", "MEDIUM": "#f1c21b"}
    diff_cols = st.columns(2)

    for i, r in enumerate(worst):
        col = diff_cols[i % 2]
        with col:
            tx_label = r["transaction_type"].replace("_", " ").title()
            anomaly_badge = ""
            if r.get("anomaly"):
                sigma = r.get("anomaly_sigma", 0)
                anomaly_badge = f"&nbsp;<span style='background:#2a1200;color:#ff832b;font-size:10px;font-weight:600;padding:1px 6px;border:1px solid #ff832b'>⚠ ANOMALY {sigma}σ</span>"
            st.markdown(
                f"<div style='background:#262626;border:1px solid #393939;border-bottom:none;"
                f"padding:8px 12px;font-family:IBM Plex Mono,monospace;font-size:11px;color:#8d8d8d'>"
                f"{r['transaction_id']} &nbsp;·&nbsp; {tx_label} &nbsp;·&nbsp; ${r['amount']:,.2f} {r['currency']}{anomaly_badge}"
                f"</div>",
                unsafe_allow_html=True,
            )
            for d in r["divergences"]:
                sev_c = sev_colors.get(d["severity"], "#8d8d8d")
                field_label = d["field"].replace("_", " ").upper()
                legacy_val = f"${d['legacy']:.4f}" if isinstance(d["legacy"], float) else str(d["legacy"])
                modern_val = f"${d['modern']:.4f}" if isinstance(d["modern"], float) else str(d["modern"])
                diff_val = f"${d['diff']:.4f}" if isinstance(d.get("diff"), float) else str(d.get("diff", "—"))
                reg = d.get("regulation", "")

                lc, mc = st.columns(2)
                with lc:
                    st.markdown(
                        f"<div style='background:#1c1c1c;border:1px solid #393939;border-right:none;padding:8px 12px'>"
                        f"<div style='font-size:9px;color:#6f6f6f;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px'>LEGACY · {field_label}</div>"
                        f"<div style='font-family:IBM Plex Mono,monospace;font-size:14px;color:#fa4d56;font-weight:500'>{legacy_val}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                with mc:
                    st.markdown(
                        f"<div style='background:#1c1c1c;border:1px solid #393939;padding:8px 12px'>"
                        f"<div style='font-size:9px;color:#6f6f6f;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px'>MODERN · {field_label}</div>"
                        f"<div style='font-family:IBM Plex Mono,monospace;font-size:14px;color:#42be65;font-weight:500'>{modern_val}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f"<div style='background:#1a1a1a;border:1px solid #393939;border-top:none;"
                    f"padding:5px 12px;font-family:IBM Plex Mono,monospace;font-size:11px;margin-bottom:4px'>"
                    f"<span style='color:#f1c21b'>Δ {diff_val}</span>"
                    f"&nbsp;&nbsp;<span style='color:{sev_c};font-weight:600'>{d['severity']}</span>"
                    f"&nbsp;&nbsp;<span style='color:#6f6f6f;font-size:10px'>{reg}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Divergence log table ───────────────────────────────────────────────────────
st.markdown('<div class="ibm-section-header">Divergence Log</div>', unsafe_allow_html=True)

if divergent:
    rows = []
    for r in divergent[:50]:
        for d in r["divergences"]:
            rows.append({
                "Transaction ID": r["transaction_id"],
                "Type": r["transaction_type"].replace("_", " ").title(),
                "Amount": f"${r['amount']:,.2f} {r['currency']}",
                "Field": d["field"],
                "Legacy": d["legacy"],
                "Modern": d["modern"],
                "Diff": d.get("diff", "—"),
                "Severity": d["severity"],
                "Anomaly": f"{r.get('anomaly_sigma', 0):.1f}σ" if r.get("anomaly") else "—",
                "Regulation": d.get("regulation", "—"),
            })
    df_div = pd.DataFrame(rows)

    def colour_sev(val):
        return {"CRITICAL": "color:#fa4d56;font-weight:600", "HIGH": "color:#ff832b;font-weight:600", "MEDIUM": "color:#f1c21b"}.get(val, "")

    st.dataframe(
        df_div.style.applymap(colour_sev, subset=["Severity"]),
        use_container_width=True,
        hide_index=True,
        height=min(400, 40 + len(rows) * 35),
    )
else:
    st.markdown('<div style="color:#42be65;background:#022b1a;border:1px solid #42be65;padding:12px 16px;font-size:13px">No divergences detected — all functions at 100% parity.</div>', unsafe_allow_html=True)

# ── Bob recommendation ────────────────────────────────────────────────────────
st.markdown('<div class="ibm-section-header">Cutover Recommendation</div>', unsafe_allow_html=True)

safe    = [s["function"] for s in scores if s["verdict"] == "SAFE_TO_CUT"]
monitor = [s["function"] for s in scores if s["verdict"] == "CUT_WITH_MONITORING"]
hold    = [s["function"] for s in scores if s["verdict"] in ("HOLD_INVESTIGATE", "DO_NOT_CUT")]

rec1, rec2, rec3 = st.columns(3)
with rec1:
    items = "".join(f"<div style='margin:4px 0;font-family:IBM Plex Mono,monospace;font-size:12px'>✓ {f}</div>" for f in safe) if safe else "<div style='color:#6f6f6f;font-size:12px'>None cleared</div>"
    st.markdown(f"""<div style='background:#022b1a;border:1px solid #42be65;padding:16px'>
        <div style='color:#42be65;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>Cut Over Now</div>
        {items}</div>""", unsafe_allow_html=True)
with rec2:
    items = "".join(f"<div style='margin:4px 0;font-family:IBM Plex Mono,monospace;font-size:12px'>~ {f}</div>" for f in monitor) if monitor else "<div style='color:#6f6f6f;font-size:12px'>None</div>"
    st.markdown(f"""<div style='background:#2a1f00;border:1px solid #f1c21b;padding:16px'>
        <div style='color:#f1c21b;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>Cut with Monitoring</div>
        {items}</div>""", unsafe_allow_html=True)
with rec3:
    items = "".join(f"<div style='margin:4px 0;font-family:IBM Plex Mono,monospace;font-size:12px'>✗ {f}</div>" for f in hold) if hold else "<div style='color:#6f6f6f;font-size:12px'>None blocked</div>"
    st.markdown(f"""<div style='background:#2d0709;border:1px solid #fa4d56;padding:16px'>
        <div style='color:#fa4d56;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>Blocked — Do Not Cut</div>
        {items}</div>""", unsafe_allow_html=True)

st.markdown(f"""
<div style='margin-top:12px;background:#262626;border-left:4px solid #0f62fe;padding:12px 16px;font-size:12px;color:#8d8d8d;font-family:IBM Plex Mono,monospace'>
Bob the Judge · {total_txns:,} transactions · {len(scores)} functions · parity {overall_parity:.1f}% · exposure ${total_exposure:,.0f} · run {run_ts.strftime('%Y-%m-%d %H:%M UTC')}
</div>
""", unsafe_allow_html=True)

# ── Ask Bob ───────────────────────────────────────────────────────────────────
st.markdown('<div class="ibm-section-header">Ask Bob</div>', unsafe_allow_html=True)

bob_col1, bob_col2 = st.columns([1, 3])

with bob_col1:
    bob_mode = st.selectbox(
        "Operating Mode",
        options=["plan", "ask", "code", "orchestrator"],
        format_func=lambda x: {
            "plan":         "Plan — Migration strategy",
            "ask":          "Ask — Explain verdicts",
            "code":         "Code — Generate fix",
            "orchestrator": "Orchestrator — Full pipeline",
        }[x],
    )
    ask_bob_btn = st.button("Ask Bob")

with bob_col2:
    mode_prompts = {
        "plan": "Create a phased migration cutover plan based on current parity analysis.",
        "ask": "Explain the cutover verdicts and what the team should do next.",
        "code": "Generate the code fix needed to resolve the highest-severity divergence.",
        "orchestrator": "Orchestrate the full cutover pipeline across all payment functions.",
    }
    bob_context = {
        "scores": scores,
        "total_txns": total_txns,
        "overall_parity": round(overall_parity, 1),
        "exposure_usd": total_exposure,
    }

    if ask_bob_btn:
        with st.spinner(f"Bob ({bob_mode}) processing..."):
            response = ask_bob(bob_mode, mode_prompts[bob_mode], bob_context)
            st.session_state["bob_response"] = response

    if "bob_response" in st.session_state:
        resp = st.session_state["bob_response"]
        is_live = resp.get("source") != "mock"
        tag_class = "bob-source-live" if is_live else "bob-source-mock"
        tag_text = "● LIVE — IBM Bob API" if is_live else "○ IBM Bob API — connecting at hackathon kickoff"
        st.markdown(f"""
        <div class="bob-panel">
            <div class="{tag_class}">{tag_text}</div>
            &nbsp;·&nbsp; <span style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#6f6f6f'>mode:{resp['mode']} &nbsp; session:{resp['session_id']}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(resp["content"])

# ── Live streaming mode ───────────────────────────────────────────────────────
if live_mode:
    st.markdown('<div class="ibm-divider"></div>', unsafe_allow_html=True)
    countdown_ph = st.empty()
    for remaining in range(5, 0, -1):
        countdown_ph.markdown(
            f'<div style="text-align:center;font-family:IBM Plex Mono,monospace;font-size:12px;color:#6f6f6f">'
            f'<span class="live-badge">LIVE</span> &nbsp; Next refresh in {remaining}s</div>',
            unsafe_allow_html=True,
        )
        time.sleep(1)
    st.rerun()
