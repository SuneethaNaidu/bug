"""Explainable rule-based priority recommendation."""
import re

def recommend_priority(title, description="", existing_priority=None):
    text = f"{title or ''} {description or ''}".lower()
    if existing_priority and str(existing_priority).strip().lower() in {"critical", "high", "medium", "low"}:
        # Preserve known labels as a baseline recommendation, rather than silently replacing them.
        return str(existing_priority).strip().title(), "Preserved existing priority label."
    critical_terms = ["data loss", "security breach", "remote code execution", "production down", "service unavailable", "payment failure"]
    high_terms = ["crash", "cannot login", "can't login", "login fails", "blocks all users", "corrupt"]
    medium_terms = ["incorrect", "fails when", "error", "exception", "not working"]
    if any(term in text for term in critical_terms):
        return "Critical", "Rule matched a potentially severe phrase; human review required."
    if any(term in text for term in high_terms):
        return "High", "Rule matched a crash, access failure, or blocking symptom."
    if any(term in text for term in medium_terms):
        return "Medium", "Rule matched an explicit error or failure symptom."
    return "Low", "No high-severity phrase detected by the configured baseline rules."
