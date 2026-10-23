import streamlit as st
from services.data_service import load_sample_data
from agents.orchestrator import run_triage

st.set_page_config(page_title="Issue Explorer | TriageFlow AI", page_icon="🔎", layout="wide")
st.title("🔎 Issue Explorer")
df = st.session_state.get("triage")
if df is None:
    st.info("No triage results yet. Run analysis on the Home page.")
    st.stop()
query = st.text_input("Search title, description, ID, or team")
cats = ["All"] + sorted(df["predicted_category"].dropna().astype(str).unique().tolist())
selected_cat = st.selectbox("Category", cats)
priorities = ["All"] + sorted(df["recommended_priority"].dropna().astype(str).unique().tolist())
selected_priority = st.selectbox("Priority", priorities)
filtered = df.copy()
if query:
    mask = filtered.astype(str).apply(lambda col: col.str.contains(query, case=False, na=False)).any(axis=1)
    filtered = filtered[mask]
if selected_cat != "All":
    filtered = filtered[filtered["predicted_category"] == selected_cat]
if selected_priority != "All":
    filtered = filtered[filtered["recommended_priority"] == selected_priority]
st.write(f"Showing {len(filtered)} issue(s)")
st.dataframe(filtered, use_container_width=True, hide_index=True)
