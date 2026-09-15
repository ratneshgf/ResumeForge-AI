# Local setup

## Backend

Use Python 3.10 or 3.11 with the pinned dependencies in `backend/requirements.txt`.
From the project directory, run these commands in PowerShell:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env  # Only if .env does not already exist
python ../setup.py
uvicorn app.main:app --reload --port 8000
```

Before starting the backend, edit `.env`:

- Set `GEMINI_API_KEY` or `OPENAI_API_KEY` and select `AI_PROVIDER`.
- Keep `ENV=development` and `FRONTEND_ORIGIN=http://localhost:5173`.
- Keep `USE_REDIS=false` for in-memory sessions.
- Configure `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` if using payments.

The setup script downloads the NLP models and creates storage directories.
If model downloads fail, run:

```powershell
python -m spacy download en_core_web_md
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

Check http://localhost:8000/health and http://localhost:8000/docs.

## Frontend

In a separate terminal with Node.js 18 or newer:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The frontend connects to http://localhost:8000
by default. If configuring `VITE_API_URL`, use the local backend URL.
If port 5173 is occupied, free it before starting the frontend so the
backend's configured origin matches.

## Optional Redis

To use an installed local Redis server, set `USE_REDIS=true` and
`REDIS_URL=redis://localhost:6379/0`. It is unnecessary for the default
in-memory configuration.

## Checks

```powershell
# From backend, with its virtual environment activated
python check_models.py

# From frontend
npm run build
```

Uploaded and generated files are temporary and removed by the cleanup task.
Keep real credentials in `.env` and avoid committing them.
