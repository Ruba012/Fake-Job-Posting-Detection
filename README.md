# Fake Job Posting Detection

[Live website](https://fakejobpostingdetector.com/)

This was built as a Senior Project II team project. The app takes a job title and description, then predicts whether the posting is **Fake** or **Real**.

## Prediction process

1. The backend joins the title and description.
2. It lowercases the text and removes numbers and punctuation.
3. A TF-IDF vectorizer extracts 5,000 unigram and bigram features.
4. Four binary features are added: salary mentioned, company logo, screening questions, and remote work.
5. The model returns a label and confidence score. The posting and result are saved in SQLite.

The training feature matrix has 17,880 rows and 5,004 columns. In the current web form, salary and remote-work indicators are derived from the text. The logo and screening-question indicators are set to 0 because the form does not collect them.

## Run locally

Use Python 3.11. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FJPD_ADMIN_USERNAME = "admin"
$env:FJPD_ADMIN_PASSWORD = "change-this-password"
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000.

## Repository contents

- `backend/`: FastAPI app, prediction code, database functions, and trained model files.
- `frontend/`: web interface.
- `docs/`: feature summary and project figures.

The source datasets and project report are not included. Predictions can be wrong and should not be treated as proof that a posting is safe or fraudulent.

**Admin note:** The dashboard API routes do not currently use session-based authentication.
