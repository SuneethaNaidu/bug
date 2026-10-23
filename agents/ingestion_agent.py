"""Issue ingestion helpers."""
from services.data_service import normalize_columns, validate_issues

def ingest_dataframe(df):
    normalized = normalize_columns(df)
    clean, report = validate_issues(normalized)
    return clean, report
