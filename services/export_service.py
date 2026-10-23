"""Export helpers."""
from io import BytesIO
import pandas as pd

def csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")
