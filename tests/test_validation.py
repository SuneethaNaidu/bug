import pandas as pd
from services.data_service import normalize_columns, validate_issues

def test_schema_normalization_and_validation():
    df = pd.DataFrame([{"summary":"Crash on login","body":"boom"},{"summary":"","body":"empty title"}])
    normalized = normalize_columns(df)
    clean, report = validate_issues(normalized)
    assert len(clean) == 1
    assert report["blank_titles_removed"] == 1
