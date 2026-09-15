# Deploy: Vercel frontend + Render backend

This guide assumes you publish the Git repository inside `resumeforge-project`
(the repository already has the GitHub remote `ratneshgf/ResumeForge-AI`).
That repository contains `backend/`, `frontend/`, and `render.yaml` at its root.
Do not import the outer workspace repository containing two nested Git repositories.
Docker is not required.

## 1. Publish the prepared changes

Review, commit, and push the changes from the project repository to GitHub.
Keep `backend/.env` private; the hosting platforms do not receive this ignored file.
Configure credentials through their dashboards.

## 2. Create the Render backend

In Render, select **New > Blueprint**, connect the GitHub repository, and use
`render.yaml`. The blueprint uses a free instance for a demo. This backend
loads PyTorch, spaCy's medium model, and Sentence Transformers: 512 MB may be
insufficient. For reliable model inference, select a paid instance with at least
2 GB RAM and verify memory usage under load; increase RAM if needed.

When prompted, enter:

- `FRONTEND_ORIGIN`: your exact production Vercel origin, e.g.
  `https://your-project.vercel.app` (no path or trailing slash). You can change
  this after Vercel assigns its URL.
- `GEMINI_API_KEY`: your Gemini key.

For OpenAI instead, add `OPENAI_API_KEY`, change `AI_PROVIDER` to `openai`, and
leave the unused Gemini key empty. For real payments, add `RAZORPAY_KEY_ID`
and `RAZORPAY_KEY_SECRET` in Render. Without these, the app uses mock payments.

If creating a Web Service manually, use:

| Setting | Value |
| --- | --- |
| Runtime | Python |
| Root directory | `backend` |
| Build command | `bash build.sh` |
| Start command | `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1` |
| Health check | `/health` |
| `PYTHON_VERSION` | `3.11.11` |
| `ENV` | `production` |
| `USE_REDIS` | `false` |
| `SPACY_MODEL` | `en_core_web_md` |
| `SENTENCE_TRANSFORMER_MODEL` | `models/all-MiniLM-L6-v2` |
| `NLTK_DATA` | `./nltk_data` |
| `TOKENIZERS_PARALLELISM` | `false` |
| `OMP_NUM_THREADS` | `1` |

Also supply the origin and provider credentials described above.
The build installs CPU-only PyTorch and downloads the models before startup.
Copy the backend URL assigned by Render and check `https://YOUR-BACKEND.onrender.com/health`.

## 3. Create the Vercel frontend

In Vercel, select **Add New > Project** and import the same GitHub repository.

| Setting | Value |
| --- | --- |
| Framework | Vite |
| Root directory | `frontend` |
| Install command | `npm ci` |
| Build command | `npm run build` |
| Output directory | `dist` |
| Environment variable | `VITE_API_URL=https://YOUR-BACKEND.onrender.com` |

Set `VITE_API_URL` for Production before deploying. Set it for Preview too
if you want preview builds, but the backend only allows the configured origin.
Use the Render URL without a trailing slash. Vercel's `vercel.json` handles
React Router deep links. Changing a Vite environment variable requires redeploying.
Never put AI or payment secrets in `VITE_*` variables: these are public browser assets.

## 4. Connect and verify

Set Render's `FRONTEND_ORIGIN` to Vercel's assigned production URL and redeploy
the backend. Keep the local `.env` configured for localhost.

- Check the Render `/health` endpoint.
- Open Vercel and refresh `/upload` directly to confirm routing works.
- Upload a resume, analyze a job description, enhance, and download.
- If requests fail with CORS errors, check the origin matches exactly.
- If Render logs show an out-of-memory termination, increase instance RAM.

Sessions are held in memory and files are temporary. Keep one worker and one
instance. Restarts and redeploys lose active sessions/uploads; free services
also sleep after 15 idle minutes. `USE_REDIS` does not implement shared session
storage in this version, so enabling it does not make multiple instances safe.

References: [Render Blueprint](https://render.com/docs/blueprint-spec),
[Python version](https://render.com/docs/python-version),
[Render free limits](https://render.com/docs/free),
[Vite on Vercel](https://vercel.com/docs/frameworks/frontend/vite).
