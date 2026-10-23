import streamlit as st
import pandas as pd
from models.evaluate_models import evaluate_categories

st.set_page_config(page_title="Model Evaluation | TriageFlow AI", page_icon="🧪", layout="wide")
st.title("🧪 Model Evaluation")
source = st.session_state.get("issues")
if source is None:
    st.info("Load a dataset on the Home page.")
    st.stop()
if "category" not in source or source["category"].fillna("").astype(str).str.strip().eq("").all():
    st.warning("The current dataset has no ground-truth category labels. Evaluation metrics cannot be honestly calculated yet.")
    st.write("Upload a labeled issue export containing a `category` column to evaluate a supervised classifier.")
else:
    if st.button("Evaluate category classifier", type="primary"):
        result = evaluate_categories(source)
        st.session_state.evaluation_result = result
    result = st.session_state.get("evaluation_result")
    if result:
        if result.get("evaluated"):
            st.metric("Held-out accuracy", f"{result['accuracy']:.1%}")
            st.write(f"Test records: {result['test_records']}")
            st.markdown("#### Classification report")
            st.dataframe(pd.DataFrame(result["classification_report"]).T, use_container_width=True)
            st.markdown("#### Confusion matrix")
            st.write(result["class_labels"])
            st.dataframe(pd.DataFrame(result["confusion_matrix"],index=result["class_labels"],columns=result["class_labels"]))
        else:
            st.info(result.get("reason","Evaluation could not be performed."))
