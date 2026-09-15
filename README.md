# ResumeForge AI

AI-powered resume optimization with ATS scoring and template preservation.
Upload a PDF or DOCX resume, analyze a target job description, enhance the
content, compare changes, and download the result.

## Run locally

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for local installation and configuration.

- Backend: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Stack

- Backend: FastAPI, spaCy, Sentence Transformers, scikit-learn, NLTK
- Documents: python-docx, PyMuPDF, ReportLab
- AI: Gemini or OpenAI
- Payments: Razorpay (optional credentials)
- Frontend: React, TypeScript, Vite, Tailwind CSS, TanStack Query

## Configuration

Copy `backend/.env.example` to `backend/.env` and configure an AI provider key.
Keep credentials in `.env`, which is ignored by Git. Session storage defaults
to memory; Redis is optional and can run on localhost.

## Limitations

PDF formatting preservation is approximate. In-memory sessions expire when
the backend restarts. AI features require a configured provider key.

## Hosting

See [RENDER_DEPLOY.md](RENDER_DEPLOY.md) for the Vercel frontend and Render backend setup.
