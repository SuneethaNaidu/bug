import streamlit as st

st.set_page_config(page_title="Settings | TriageFlow AI", page_icon="⚙️", layout="wide")
st.title("⚙️ Settings")
st.markdown("### Pipeline defaults")
threshold = st.slider("Duplicate similarity threshold", min_value=0.20, max_value=0.95, value=0.55, step=0.05)
st.write(f"Current page setting: **{threshold:.2f}**")
st.caption("To apply a different threshold to the complete pipeline, pass this value to `run_triage(df, duplicate_threshold=threshold)` in app.py.")
st.markdown("### Optional integrations")
st.info("GitHub API support is read-only in this starter project. No issue assignments, labels, or comments are written back.")
st.info("LLM API integration is intentionally optional. The core template-based explanation agent runs without a key.")
st.markdown("### Data and privacy")
st.write("Uploaded data is processed by the running app. Avoid uploading confidential issue reports to a public deployment. Review your hosting and API provider privacy terms before enabling external services.")
