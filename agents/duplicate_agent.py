"""Potential duplicate detection using TF-IDF and cosine similarity."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from agents.cleaning_agent import prepare_text

def find_duplicates(df, threshold=0.55):
    if len(df) == 0:
        return pd.DataFrame(columns=["duplicate_candidate","duplicate_similarity","duplicate_of"])
    texts = prepare_text(df).tolist()
    if len(texts) < 2 or not any(t.strip() for t in texts):
        return pd.DataFrame({"duplicate_candidate":[False]*len(df),"duplicate_similarity":[0.0]*len(df),"duplicate_of":[""]*len(df)})
    try:
        matrix = TfidfVectorizer(ngram_range=(1,2), stop_words="english").fit_transform(texts)
        sims = cosine_similarity(matrix)
    except ValueError:
        sims = [[0.0 for _ in texts] for _ in texts]
    ids = df.get("issue_id", pd.Series([str(i) for i in range(len(df))])).astype(str).tolist()
    duplicate, score, duplicate_of = [], [], []
    for i in range(len(texts)):
        row = sims[i].copy()
        row[i] = -1
        j = int(max(range(len(row)), key=lambda k: row[k]))
        value = float(row[j]) if len(row) else 0.0
        duplicate.append(value >= threshold)
        score.append(round(max(value, 0.0), 3))
        duplicate_of.append(ids[j] if value >= threshold else "")
    return pd.DataFrame({"duplicate_candidate":duplicate,"duplicate_similarity":score,"duplicate_of":duplicate_of})
