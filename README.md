# Marksheet Extraction API

FastAPI-based API to extract structured JSON from marksheet images/PDFs.

Quick start

1. Create and activate virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

3. Run app

```powershell
uvicorn app.main:app --reload --port 8000
```

API

- POST `/api/v1/extract` — multipart file upload (image/pdf). Max 10 MB.

See `app/` for implementation details.
