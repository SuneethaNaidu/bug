import streamlit as st
import plotly.express as px
import pandas as pd
from services.data_service import load_sample_data
from agents.orchestrator import run_triage

st.set_page_config(page_title="Dashboard | TriageFlow AI", page_icon="📊", layout="wide")
st.title("📊 Engineering Dashboard")
st.caption("Run a quick analytics view using the sample dataset or your current uploaded data.")
if "triage" not in st.session_state or st.session_state.triage is None:
    if st.button("Analyze sample issues"):
        st.session_state.triage = run_triage(st.session_state.get("issues", load_sample_data()))
        st.rerun()
    st.info("Run analysis from the Home page or click above to analyze the current session dataset.")
    st.stop()
df = st.session_state.triage
a,b,c,d = st.columns(4)
a.metric("Issues",len(df))
b.metric("Potential duplicates",int(df["duplicate_candidate"].sum()))
c.metric("Needs review",int((df["review_status"]=="Needs review").sum()))
d.metric("Teams",df["recommended_team"].nunique())
left,right = st.columns(2)
with left:
    st.plotly_chart(px.histogram(df,x="predicted_category",title="Issues by category",color="predicted_category"),use_container_width=True)
    st.plotly_chart(px.histogram(df,x="recommended_priority",title="Recommended priority",color="recommended_priority"),use_container_width=True)
with right:
    st.plotly_chart(px.histogram(df,x="recommended_team",title="Recommended team",color="recommended_team"),use_container_width=True)
    st.plotly_chart(px.histogram(df,x="status",title="Issues by status",color="status"),use_container_width=True)
