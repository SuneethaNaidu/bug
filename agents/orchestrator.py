"""Coordinates the triage stages and produces a reviewable result table."""
import pandas as pd
from agents.classification_agent import classify_issues
from agents.duplicate_agent import find_duplicates
from agents.priority_agent import recommend_priority
from agents.assignment_agent import recommend_team
from agents.explanation_agent import summarize_issue, explain_triage

def run_triage(df, duplicate_threshold=0.55):
    work = df.copy().reset_index(drop=True)
    if "issue_id" not in work:
        work["issue_id"] = [f"ISSUE-{i+1:04d}" for i in range(len(work))]
    for col, default in [("title","Untitled issue"),("description",""),("status","Open"),("repository",""),("labels","")]:
        if col not in work:
            work[col] = default
        work[col] = work[col].fillna(default)
    classification, model_info = classify_issues(work)
    duplicates = find_duplicates(work, threshold=duplicate_threshold)
    output = pd.concat([work, classification, duplicates], axis=1)
    priorities, priority_reasons, teams, team_reasons, summaries, explanations = [], [], [], [], [], []
    for _, row in output.iterrows():
        p, pr = recommend_priority(row.get("title"), row.get("description"), row.get("priority"))
        team, tr = recommend_team(row["predicted_category"], row.get("repository"), row.get("labels"))
        priorities.append(p); priority_reasons.append(pr); teams.append(team); team_reasons.append(tr)
        summaries.append(summarize_issue(row.get("title"), row.get("description")))
        explanations.append(explain_triage(row["predicted_category"], p, team, row["duplicate_candidate"], row["duplicate_of"], float(row["duplicate_similarity"]), row["classification_method"], pr, tr))
    output["recommended_priority"] = priorities
    output["priority_reason"] = priority_reasons
    output["recommended_team"] = teams
    output["team_reason"] = team_reasons
    output["ai_summary"] = summaries
    output["triage_explanation"] = explanations
    output["review_status"] = "Needs review"
    return output
