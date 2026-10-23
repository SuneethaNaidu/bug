"""Transparent team routing rules."""
TEAM_BY_CATEGORY = {
    "UI": "Frontend",
    "Authentication": "Identity & Access",
    "API": "API Platform",
    "Database": "Database",
    "Performance": "Performance Engineering",
    "Security": "Security",
    "Backend": "Backend",
    "Other": "Triage Queue",
}

def recommend_team(category, repository=None, labels=None):
    label_text = " ".join(labels) if isinstance(labels, list) else str(labels or "")
    repo = str(repository or "").lower()
    if "security" in label_text.lower() or "security" in repo:
        return "Security", "Repository or labels mention security."
    category = str(category or "Other")
    return TEAM_BY_CATEGORY.get(category, "Triage Queue"), f"Default routing map for category '{category}'."
