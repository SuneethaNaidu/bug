# TriageFlow AI — Agentic AI Bug Triage System

A modular Python + Streamlit mini-project demonstrating bug-report ingestion, NLP classification, rule-based priority recommendations, TF-IDF duplicate detection, team routing, triage explanations, human review, and analytics.

## Project scope

This is an educational research prototype. Its baseline classifier uses labeled data when sufficient labels are available; otherwise it uses transparent keyword rules. Priority recommendations are rule-based unless a future supervised model is added. Duplicate similarity is a candidate signal, not proof. Review recommendations before taking action.

## Features

- CSV and JSON upload with schema normalization and data-quality report
- Included sample issue dataset
- Optional read-only public GitHub Issues API client (`services/github_service.py`)
- TF-IDF + Logistic Regression category model when enough labels are present
- Keyword category fallback for small or unlabeled datasets
- Explainable priority recommendation rules
- TF-IDF cosine-similarity duplicate candidate detection
- Configurable team routing
- Issue summary and grounded template explanation (no LLM key needed)
- Dashboard, issue explorer, triage workbench, duplicate review, model evaluation, settings
- CSV export and basic tests

## Requirements

Python 3.11 is recommended. Use a virtual environment.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints the local URL, normally http://localhost:8501.

## Suggested demo

1. Start the app and keep the included sample dataset.
2. Select **Analyze all issues** on the Home page.
3. Explore the generated table, category chart, priority chart, and CSV download.
4. Open Issue Explorer and search for login issues.
5. Open Triage Workbench and save a human review decision.
6. Open Duplicate Review and inspect similarity candidates.
7. Open Model Evaluation. The included sample data has labels, but the small dataset may not satisfy every class-count requirement for reliable evaluation. The page will explain if it cannot evaluate.
8. Upload your own issue export and review the data-quality report.

## Expected CSV columns

Required: `title` or a supported alias such as `summary` or `subject`.

Recommended: `issue_id`, `title`, `description`, `labels`, `category`, `priority`, `status`, `assignee`, `team`, `created_at`, `updated_at`, `repository`, `source_url`.

The schema normalizer supports common aliases. Add mappings in `services/data_service.py` for other export formats.

## Optional GitHub Issues API

A read-only helper is included in `services/github_service.py`. It is not wired into the main UI yet; this avoids unexpected API calls during startup. To use it from a Python script:

```python
from agents.ingestion_agent import ingest_dataframe
from services.github_service import fetch_public_issues

raw = fetch_public_issues("OWNER/REPOSITORY", limit=100)
issues, report = ingest_dataframe(raw)
print(report)
```

For public repositories, a token is generally not needed. For private repositories, supply a token from an environment variable. Never hardcode or commit credentials. The helper skips pull requests and does not modify GitHub issues.

## Training and evaluation

The category classifier trains only when there are enough labeled records and multiple classes. The training helper can save a model:

```python
import pandas as pd
from models.train_models import train_and_save

df = pd.read_csv("your_labeled_issues.csv")
print(train_and_save(df))
```

The current orchestrator trains a classifier in memory for each run when the dataset is suitable. For a production application, train once, persist the model, load it with versioning, and evaluate it on a held-out test set.

Run evaluation from the UI's **Model Evaluation** page or with:

```python
from models.evaluate_models import evaluate_categories
print(evaluate_categories(df))
```

Do not report accuracy or other metrics unless calculated on appropriate labeled held-out data. Duplicate-detection evaluation requires ground-truth duplicate pairs; this starter project does not fabricate them.

## Tests

```bash
pytest -q
```

## GitHub setup

1. Create a new empty repository on GitHub.
2. In the project directory:

```bash
git init
git add .
git commit -m "Initial Agentic AI bug triage project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace the URL with your own repository URL. Do not commit `.env`, private datasets, or tokens.

## Streamlit Community Cloud deployment

1. Push the complete project to GitHub.
2. Sign in to Streamlit Community Cloud and create a new app.
3. Select your repository, branch (`main`), and main file (`app.py`).
4. Deploy and inspect the logs if dependencies or imports fail.
5. Add secrets only if a future optional integration needs them.

The sample dataset is included in the repository so the core demo does not require credentials.

## Limitations and future work

- The default priority engine uses explainable rules, not a trained priority model.
- Team routing uses category mappings and simple repository/label checks, not learned team ownership.
- The LLM explanation agent is a grounded template fallback; an external LLM integration is not wired into the UI in this starter.
- Similarity uses TF-IDF cosine similarity; embedding-based semantic search can improve recall.
- The GitHub client is a helper and read-only; it is not connected to the dashboard UI.
- Review decisions persist in the current Streamlit session only; production use should add a database.
- Production deployments should add authentication, access controls, rate limits, audit logs, and data-retention controls.

These limitations are stated explicitly so the project can be extended honestly and evaluated rigorously.
