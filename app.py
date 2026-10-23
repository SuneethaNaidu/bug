import streamlit as st
import pandas as pd
from pathlib import Path
from agents.orchestrator import run_triage
from services.data_service import load_sample_data, normalize_columns, validate_issues
from services.export_service import csv_bytes
from utils.logging_config import configure_logging

configure_logging()
st.set_page_config(page_title="TriageFlow AI", page_icon="🛠️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root { --ink:#12233f; --blue:#3978f6; --teal:#15a99a; }
.block-container {padding-top:1.6rem; padding-bottom:2.5rem; max-width:1450px;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#101d35 0%,#172b4b 100%);}
[data-testid="stSidebar"] * {color:#f2f6ff !important;}
.hero {padding:1.5rem 1.7rem;border-radius:18px;background:linear-gradient(120deg,#12233f,#24518c);color:white;margin-bottom:1.2rem;}
.hero h1 {margin:0 0 .35rem 0;font-size:2.1rem;}
.hero p {margin:0;color:#dbeafe;font-size:1rem;}
.metric-card {border:1px solid #dbe4f0;border-radius:14px;padding:1rem 1.1rem;background:linear-gradient(180deg,#fff,#f8fbff);min-height:110px;}
.metric-label {font-size:.82rem;color:#61718a;margin-bottom:.45rem;}
.metric-value {font-size:1.8rem;font-weight:750;color:#142849;}
.metric-note {font-size:.78rem;color:#74839a;margin-top:.2rem;}
.section-title {font-size:1.15rem;font-weight:700;color:#152b4a;margin:.4rem 0 .8rem 0;}
.small-muted {color:#65758b;font-size:.9rem;}
div[data-testid="stMetric"] {border:1px solid #dbe4f0;border-radius:14px;padding:12px 14px;background:#fff;}
</style>
""", unsafe_allow_html=True)

def metric_card(label, value, note="Live dataset"):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

if "issues" not in st.session_state:
    st.session_state.issues = load_sample_data()
if "triage" not in st.session_state:
    st.session_state.triage = None
if "review_decisions" not in st.session_state:
    st.session_state.review_decisions = {}

with st.sidebar:
    st.markdown("## 🛠️ TriageFlow AI")
    st.caption("Agentic bug-triage workspace")
    st.markdown("---")
    st.markdown("### Data source")
    uploaded = st.file_uploader("Upload CSV or JSON", type=["csv", "json"])
    if uploaded is not None and st.button("Load uploaded dataset", use_container_width=True):
        try:
            if uploaded.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_json(uploaded)
            df = normalize_columns(df)
            df, report = validate_issues(df)
            st.session_state.issues = df
            st.session_state.triage = None
            st.success(f"Loaded {len(df)} valid records.")
            st.session_state.data_report = report
        except Exception as exc:
            st.error(f"Could not load dataset: {exc}")
    if st.button("Restore sample dataset", use_container_width=True):
        st.session_state.issues = load_sample_data()
        st.session_state.triage = None
        st.session_state.review_decisions = {}
        st.rerun()
    st.markdown("---")
    st.caption("Core pipeline works locally without paid API credentials.")
    st.caption("LLM and live GitHub integrations are optional extensions.")

issues = st.session_state.issues.copy()
st.markdown('<div class="hero"><h1>Agentic AI Bug Triage</h1><p>Turn incoming issue reports into explainable, reviewable engineering actions.</p></div>', unsafe_allow_html=True)
st.markdown("This mini-project demonstrates issue ingestion, NLP-based classification, priority recommendations, duplicate detection, team routing, and human review.")

if "data_report" in st.session_state:
    with st.expander("Latest data-quality report"):
        st.json(st.session_state.data_report)

c1, c2, c3, c4 = st.columns(4)
open_count = int(issues["status"].astype(str).str.lower().isin(["open", "new", "in progress", "reopened"]).sum()) if "status" in issues else len(issues)
priority_series = issues.get("priority", pd.Series(dtype=str)).astype(str).str.lower()
high_count = int(priority_series.isin(["critical", "high", "p0", "p1"]).sum())
c1.markdown('<div class="section-title">Workspace overview</div>', unsafe_allow_html=True)
with c1: metric_card("Issues loaded", f"{len(issues):,}", "Current dataset")
with c2: metric_card("Open / active", f"{open_count:,}", "Based on status values")
with c3: metric_card("High / critical", f"{high_count:,}", "Existing labels")
with c4: metric_card("Potential duplicates", f"{len(st.session_state.triage) if st.session_state.triage is not None else '—'}", "Run pipeline to calculate")

st.markdown("### Run the triage pipeline")
col_run, col_info = st.columns([1, 2])
with col_run:
    run_clicked = st.button("▶ Analyze all issues", type="primary", use_container_width=True)
with col_info:
    st.markdown('<div class="small-muted">The pipeline cleans issue text, predicts categories when training labels exist, estimates priority, detects similar reports, recommends a team, and records each stage.</div>', unsafe_allow_html=True)

if run_clicked:
    with st.spinner("Running the triage pipeline..."):
        try:
            st.session_state.triage = run_triage(issues)
            st.success("Pipeline completed.")
        except Exception as exc:
            st.error(f"Pipeline failed safely: {exc}")

if st.session_state.triage is not None:
    results = st.session_state.triage
    st.markdown("### Triage results")
    left, right = st.columns([1.2, 1])
    with left:
        st.dataframe(results[["issue_id","title","predicted_category","recommended_priority","recommended_team","duplicate_candidate","duplicate_similarity","review_status"]], use_container_width=True, hide_index=True)
    with right:
        st.markdown("#### Recommended categories")
        st.bar_chart(results["predicted_category"].value_counts())
        st.markdown("#### Recommended priorities")
        st.bar_chart(results["recommended_priority"].value_counts())
    st.download_button("Download triage results (CSV)", csv_bytes(results), "triage_results.csv", "text/csv")
    st.session_state.issues = issues
else:
    st.info("Load a dataset or use the sample records, then select **Analyze all issues** to generate results.")

st.markdown("### Add a bug report")
with st.form("new_issue_form", clear_on_submit=True):
    title = st.text_input("Issue title", placeholder="Application crashes after clicking Login")
    description = st.text_area("Description", placeholder="Describe what happened, steps to reproduce, expected and actual behavior...")
    repo = st.text_input("Repository", value="sample/project")
    submit = st.form_submit_button("Analyze new issue")
if submit:
    if not title.strip():
        st.warning("Please enter an issue title.")
    else:
        new = pd.DataFrame([{"issue_id": f"NEW-{len(issues)+1}", "title": title.strip(), "description": description.strip(), "repository": repo, "status":"Open"}])
        combined = pd.concat([issues, new], ignore_index=True)
        with st.spinner("Analyzing new issue with existing reports..."):
            st.session_state.triage = run_triage(combined)
        st.session_state.issues = combined
        st.success("New issue added and analyzed. Review its recommendations in the results table.")
        st.rerun()

st.markdown("---")
st.caption("Research prototype: recommendations are decision support, not guaranteed ground truth. Review high-impact or low-confidence results before acting.")
