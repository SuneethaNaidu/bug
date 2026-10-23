"""Dataset loading, schema normalization, and validation."""
from pathlib import Path
import pandas as pd

ALIASES = {
    "number":"issue_id", "id":"issue_id", "issue number":"issue_id",
    "name":"title", "summary":"title", "subject":"title",
    "body":"description", "details":"description", "issue description":"description",
    "label":"labels", "type":"category", "severity":"priority",
    "state":"status", "owner":"assignee", "created":"created_at",
    "created date":"created_at", "repo":"repository",
}

def normalize_columns(df):
    out = df.copy()
    out.columns = [str(c).strip().lower().replace("_", " ") for c in out.columns]
    out = out.rename(columns={c: ALIASES.get(c, c.replace(" ", "_")) for c in out.columns})
    # Canonicalize columns not explicitly mapped.
    out.columns = [c.replace(" ", "_") for c in out.columns]
    if "title" not in out:
        raise ValueError("Dataset must contain a title, summary, or subject column.")
    if "description" not in out:
        out["description"] = ""
    if "issue_id" not in out:
        out["issue_id"] = [f"ISSUE-{i+1:04d}" for i in range(len(out))]
    for col, default in [("status","Open"),("repository",""),("labels",""),("priority",""),("category",""),("team",""),("assignee","")]:
        if col not in out:
            out[col] = default
    return out

def validate_issues(df):
    before = len(df)
    out = df.copy()
    out["title"] = out["title"].fillna("").astype(str).str.strip()
    out["description"] = out["description"].fillna("").astype(str)
    missing_title = int((out["title"] == "").sum())
    out = out[out["title"] != ""].copy()
    out["issue_id"] = out["issue_id"].fillna("").astype(str)
    blank_ids = out["issue_id"].eq("")
    out.loc[blank_ids, "issue_id"] = [f"ISSUE-{i+1:04d}" for i in range(int(blank_ids.sum()))]
    duplicate_ids = int(out["issue_id"].duplicated().sum())
    out = out.drop_duplicates(subset=["issue_id"], keep="first")
    report = {"records_received": before, "records_kept": len(out), "blank_titles_removed": missing_title,
              "duplicate_ids_removed": duplicate_ids, "records_removed_total": before-len(out)}
    return out.reset_index(drop=True), report

def load_sample_data():
    path = Path(__file__).resolve().parents[1] / "data" / "sample_issues.csv"
    return normalize_columns(pd.read_csv(path))
