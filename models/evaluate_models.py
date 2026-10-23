"""Held-out evaluation utilities for labeled category data."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from agents.cleaning_agent import prepare_text

def evaluate_categories(df, test_size=0.25, random_state=42):
    if "category" not in df:
        return {"evaluated": False, "reason": "No ground-truth category column."}
    work = df[df["category"].notna()].copy()
    work["category"] = work["category"].astype(str).str.strip()
    work = work[work["category"] != ""]
    if len(work) < 10 or work["category"].nunique() < 2:
        return {"evaluated": False, "reason": "Need at least 10 labeled rows and two classes."}
    counts = work["category"].value_counts()
    if counts.min() < 2:
        return {"evaluated": False, "reason": "Each category needs at least two records for a stratified split."}
    x = prepare_text(work)
    y = work["category"]
    try:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state, stratify=y)
        model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2), stop_words="english")), ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))])
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        return {"evaluated": True, "test_records": len(y_test), "accuracy": round(float(accuracy_score(y_test,pred)),4),
                "classification_report": classification_report(y_test,pred,output_dict=True,zero_division=0),
                "confusion_matrix": confusion_matrix(y_test,pred,labels=model.classes_).tolist(),
                "class_labels": model.classes_.tolist()}
    except Exception as exc:
        return {"evaluated": False, "reason": str(exc)}
