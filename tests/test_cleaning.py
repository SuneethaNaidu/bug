import pandas as pd
from agents.cleaning_agent import clean_text, prepare_text

def test_clean_text_normalizes_whitespace():
    assert clean_text("  HELLO\n world ") == "hello world"

def test_prepare_text_combines_fields():
    df = pd.DataFrame([{"title":"Login fails","description":"Server error"}])
    assert "login fails" in prepare_text(df).iloc[0]
