import pandas as pd
from agents.duplicate_agent import find_duplicates

def test_duplicate_detection_finds_similar_text():
    df = pd.DataFrame([
        {"issue_id":"1","title":"Login page crashes","description":"App crashes when clicking login"},
        {"issue_id":"2","title":"Login page crashes","description":"App crashes when clicking login"},
        {"issue_id":"3","title":"Change button color","description":"Make the submit button blue"},
    ])
    result = find_duplicates(df, threshold=0.5)
    assert bool(result.loc[0,"duplicate_candidate"])
    assert result.loc[0,"duplicate_of"] == "2"
