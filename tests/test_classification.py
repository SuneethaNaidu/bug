import pandas as pd
from agents.classification_agent import classify_issues

def test_classification_returns_expected_columns():
    df = pd.DataFrame([{"title":"Login password error","description":"Cannot sign in"}])
    result, info = classify_issues(df)
    assert "predicted_category" in result
    assert len(result) == 1
