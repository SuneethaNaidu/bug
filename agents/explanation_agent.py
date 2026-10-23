"""Grounded template explanations; no external LLM required."""
def summarize_issue(title, description):
    title = str(title or "Untitled issue").strip()
    description = str(description or "").strip()
    if not description:
        return f"{title}. No description was supplied; request reproduction steps and expected versus actual behavior."
    clean = " ".join(description.split())
    if len(clean) > 280:
        clean = clean[:277].rstrip() + "..."
    return f"{title}: {clean}"

def explain_triage(category, priority, team, duplicate, duplicate_of, similarity, category_method, priority_reason, team_reason):
    duplicate_text = f"Possible match with issue {duplicate_of} (similarity {similarity:.3f}); verify before linking." if duplicate else "No candidate crossed the configured duplicate threshold."
    return (
        f"Category: {category}. Method: {category_method}. "
        f"Priority: {priority}. Rationale: {priority_reason} "
        f"Recommended team: {team}. Routing rationale: {team_reason} "
        f"{duplicate_text} Recommendations are advisory and should be reviewed."
    )
