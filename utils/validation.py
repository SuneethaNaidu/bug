"""Simple reusable validation helpers."""
ALLOWED_PRIORITIES = {"critical", "high", "medium", "low"}

def valid_priority(value):
    return str(value or "").strip().lower() in ALLOWED_PRIORITIES
