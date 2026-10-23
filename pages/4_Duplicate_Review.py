import streamlit as st
import pandas as pd

st.set_page_config(page_title="Duplicate Review | TriageFlow AI", page_icon="🧬", layout="wide")
st.title("🧬 Duplicate Review")
df = st.session_state.get("triage")
if df is None:
    st.info("Run the pipeline first.")
    st.stop()
dupes = df[df["duplicate_candidate"]].copy()
st.caption("Similarity is a screening signal, not proof that two issues are duplicates. Confirm each match manually.")
if dupes.empty:
    st.success("No pairs crossed the current similarity threshold.")
else:
    st.dataframe(dupes[["issue_id","title","duplicate_of","duplicate_similarity","source_url"] if "source_url" in dupes else ["issue_id","title","duplicate_of","duplicate_similarity"]],use_container_width=True,hide_index=True)
    selected = st.selectbox("Review candidate", dupes["issue_id"].astype(str).tolist())
    decision = st.radio("Decision", ["Confirm duplicate","Not a duplicate"], horizontal=True)
    if st.button("Save duplicate decision"):
        decisions = st.session_state.get("duplicate_decisions", {})
        decisions[selected] = decision
        st.session_state.duplicate_decisions = decisions
        st.success("Saved for this session.")
    if st.session_state.get("duplicate_decisions"):
        st.dataframe(pd.DataFrame([{"issue_id":k,"decision":v} for k,v in st.session_state.duplicate_decisions.items()]),use_container_width=True)
