"""Text cleaning and feature preparation."""
import re
import pandas as pd

def clean_text(value):
    if pd.isna(value):
        return ""
    text = str(value).lower().strip()
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def prepare_text(df):
    title = df.get("title", pd.Series([""] * len(df))).fillna("").astype(str)
    description = df.get("description", pd.Series([""] * len(df))).fillna("").astype(str)
    return (title + " " + description).map(clean_text)
