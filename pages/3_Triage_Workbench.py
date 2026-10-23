import streamlit as st
import pandas as pd

st.set_page_config(page_title="Triage Workbench | TriageFlow AI", page_icon="🧰", layout="wide")
st.title("🧰 Triage Workbench")
df = st.session_state.get("triage")
if df is None or df.empty:
    st.info("Run the pipeline from the Home page first.")
    st.stop()
ids = df["issue_id"].astype(str).tolist()
selected = st.selectbox("Choose an issue", ids)
row = df[df["issue_id"].astype(str) == selected].iloc[0]
st.subheader(str(row.get("title","Untitled issue")))
st.write(row.get("description",""))
a,b,c = st.columns(3)
a.metric("Category", str(row["predicted_category"]))
b.metric("Priority", str(row["recommended_priority"]))
c.metric("Recommended team", str(row["recommended_team"]))
st.markdown("**Summary**")
st.write(row["ai_summary"])
st.markdown("**Explanation**")
st.write(row["triage_explanation"])
st.markdown("**Duplicate candidate**")
st.write(f"{row['duplicate_candidate']} — similar issue: {row['duplicate_of'] or 'None'} — similarity: {row['duplicate_similarity']}")
with st.form("review_form"):
    category = st.selectbox("Final category", sorted(set(df["predicted_category"].astype(str))), index=sorted(set(df["predicted_category"].astype(str))).index(str(row["predicted_category"])))
    priority = st.selectbox("Final priority", ["Critical","High","Medium","Low"], index=["Critical","High","Medium","Low"].index(str(row["recommended_priority"])))
    team = st.text_input("Final team", value=str(row["recommended_team"]))
    status = st.selectbox("Review decision", ["Approved","Edited","Rejected"])
    notes = st.text_area("Reviewer notes")
    save = st.form_submit_button("Save review decision")
if save:
    decisions = st.session_state.get("review_decisions", {})
    decisions[selected] = {"category":category,"priority":priority,"team":team,"status":status,"notes":notes}
    st.session_state.review_decisions = decisions
    st.success("Review decision saved in this Streamlit session.")
if st.session_state.get("review_decisions"):
    st.markdown("### Saved review decisions")
    st.dataframe(pd.DataFrame([{"issue_id":k,**v} for k,v in st.session_state.review_decisions.items()]),use_container_width=True)
