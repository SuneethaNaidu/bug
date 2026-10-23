"""Train and persist the category classifier when labels are sufficient."""
from pathlib import Path
import joblib
from agents.classification_agent import train_category_model
from services.data_service import normalize_columns

def train_and_save(df, output_path="artifacts/category_model.joblib"):
    normalized = normalize_columns(df)
    model, info = train_category_model(normalized)
    if model is None:
        return info
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    info["saved_to"] = str(path)
    return info
