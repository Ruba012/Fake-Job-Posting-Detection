# Fake Job Posting Detection

A machine-learning prototype that classifies job postings as **fake** or **real**. It includes a FastAPI backend, a single-page web interface, and the trained TF-IDF model artifacts.

**Live Demo:** [fakejobpostingdetector.com](https://fakejobpostingdetector.com/)

## Features

- Analyze a job posting from its title and description.
- Return a prediction and confidence score from the trained classifier.
- Store analyses and feedback in a local SQLite database.
- View prototype dashboard statistics and records.

## Requirements

- Python 3.11
- Packages listed in `requirements.txt`

## Run locally

From the repository root, install dependencies and configure the prototype admin login:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FJPD_ADMIN_USERNAME = "admin"
$env:FJPD_ADMIN_PASSWORD = "change-this-password"
uvicorn backend.main:app --reload
```

Then open <http://127.0.0.1:8000>. The SQLite database is created locally on first start.

## Model files

The trained classifier and TF-IDF vectorizer are stored in `backend/model/` and loaded when the API starts. They were serialized with scikit-learn; use compatible package versions when loading them.

## Project notes

- The figures in `docs/figures/` and feature summary in `docs/` describe the project inputs.
- The datasets and student report are not included in this repository.
- This is an academic prototype. The dashboard routes do not implement session-based authorization; do not expose the service publicly without adding proper authentication and access control.
- No license is included. All rights remain with the project contributors unless they choose a license.
