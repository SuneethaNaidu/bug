"""Optional GitHub Issues API client. Read-only by design."""
import requests
import pandas as pd

def fetch_public_issues(owner_repo, token=None, limit=100):
    if "/" not in owner_repo:
        raise ValueError("Repository must be in owner/repository format.")
    owner, repo = owner_repo.strip().split("/", 1)
    headers = {"Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    rows, page = [], 1
    while len(rows) < min(limit, 300):
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers=headers, params={"state":"all","per_page":100,"page":page}, timeout=20)
        response.raise_for_status()
        items = response.json()
        if not items: break
        for item in items:
            if "pull_request" in item:
                continue
            rows.append({
                "issue_id": str(item.get("number")),
                "title": item.get("title",""),
                "description": item.get("body") or "",
                "labels": [x.get("name","") for x in item.get("labels",[])],
                "status": item.get("state","Open").title(),
                "assignee": (item.get("assignee") or {}).get("login",""),
                "created_at": item.get("created_at",""),
                "updated_at": item.get("updated_at",""),
                "repository": owner_repo,
                "source_url": item.get("html_url","")
            })
        if len(items) < 100: break
        page += 1
    return pd.DataFrame(rows[:limit])
