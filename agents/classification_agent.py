"""Bug category classification with a trained model or transparent keyword fallback."""
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from agents.cleaning_agent import prepare_text

CATEGORY_KEYWORDS = {
    "Authentication": ["login", "log in", "password", "auth", "sign in", "token"],
    "UI": ["button", "layout", "css", "display", "screen", "visual", "font"],
    "API": ["endpoint", "api", "request", "response", "http", "rest"],
    "Database": ["database", "sql", "query", "migration", "postgres", "mongo"],
    "Performance": ["slow", "latency", "timeout", "memory", "performance", "hang"],
    "Security": ["security", "vulnerability", "permission", "unauthorized", "injection"],
    "Backend": ["server", "exception", "crash", "worker", "service", "backend"],
}

def keyword_category(text):
    text = str(text).lower()
    scores = {cat: sum(1 for term in terms if term in text) for cat, terms in CATEGORY_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Other"

def train_category_model(df):
    if "category" not in df:
        return None, {"trained": False, "reason": "No category labels in dataset."}
    work = df[df["category"].notna()].copy()
    work["category"] = work["category"].astype(str).str.strip()
    work = work[work["category"] != ""]
    if len(work) < 8 or work["category"].nunique() < 2 or work["category"].value_counts().min() < 2:
        return None, {"trained": False, "reason": "Need at least 8 labeled records, at least two categories, and two examples per category."}
    x = prepare_text(work)
    y = work["category"]
    model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=12000, stop_words="english")), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    try:
        model.fit(x, y)
        return model, {"trained": True, "training_records": len(work), "classes": sorted(y.unique().tolist()), "note": "For a formal report, evaluate on a held-out split before claiming model performance."}
    except Exception as exc:
        return None, {"trained": False, "reason": str(exc)}

def classify_issues(df):
    text = prepare_text(df)
    model, model_info = train_category_model(df)
    if model is not None:
        predicted = model.predict(text)
        try:
            probs = model.predict_proba(text)
            confidence = probs.max(axis=1)
        except Exception:
            confidence = [None] * len(df)
        method = "TF-IDF + Logistic Regression (trained on supplied labels)"
    else:
        predicted = [keyword_category(t) for t in text]
        confidence = [None] * len(df)
        method = "Transparent keyword fallback (not a trained ML prediction)"
    return pd.DataFrame({"predicted_category": predicted, "category_confidence": confidence, "classification_method": method}), model_info
