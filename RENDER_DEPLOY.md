# 🚀 Deploy to Render - Fixed for PyMuPDF Issue

This guide fixes the PyMuPDF compilation error on Render.

## The Problem

PyMuPDF was trying to compile from source on Render, causing build failures.

## The Solution

We've created a special `requirements-render.txt` with pre-compiled versions that work on Render.

---

## 📋 Quick Deploy to Render

### Step 1: Prepare Your Repository

Make sure all changes are pushed to GitHub:

```bash
cd d:\downloads\ResumeForge_AI_Project\resumeforge-project
git add .
git commit -m "Fix Render deployment - use binary wheels for PyMuPDF"
git push origin main
```

### Step 2: Deploy Backend to Render

#### Option A: Using render.yaml (Recommended)

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. **Add Secret Environment Variables:**
   - `GEMINI_API_KEY` = your_actual_api_key
   - `FRONTEND_ORIGIN` = (leave blank for now, update after frontend)
6. Click **"Apply"**

#### Option B: Manual Setup

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. Click **"New +"** → **"Web Service"**
3. **Connect GitHub Repository**
4. **Configure:**
   - **Name:** `resumeforge-backend`
   - **Region:** Oregon (or closest to you)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:**
     ```bash
     pip install --upgrade pip && pip install -r requirements-render.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

5. **Environment Variables:**
   ```
   ENV=production
   PYTHON_VERSION=3.11.0
   GEMINI_API_KEY=your_actual_api_key_here
   AI_PROVIDER=gemini
   AI_MAX_RETRIES=5
   AI_TIMEOUT_SECONDS=90
   AI_TEMPERATURE=0.7
   USE_REDIS=false
   MAX_UPLOAD_MB=5
   FILE_TTL_MINUTES=60
   RATE_LIMIT_PER_MINUTE=30
   LOG_LEVEL=INFO
   ```

6. **Click "Create Web Service"**

7. **Wait for Build** (5-10 minutes first time)

8. **Copy Backend URL** (e.g., `https://resumeforge-backend.onrender.com`)

---

### Step 3: Deploy Frontend to Vercel

1. **Go to [Vercel](https://vercel.com)**
2. **New Project** → Import your GitHub repo
3. **Settings:**
   - **Root Directory:** `frontend`
   - **Framework:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. **Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
   *(Use the URL from Step 2)*

5. **Deploy**

6. **Copy Frontend URL** (e.g., `https://resumeforge.vercel.app`)

---

### Step 4: Update Backend CORS

1. Go back to **Render Dashboard**
2. Select your backend service
3. Go to **"Environment"**
4. Add/Update:
   ```
   FRONTEND_ORIGIN=https://your-frontend-url.vercel.app
   ```
5. **Save** → Service will auto-redeploy

---

## ✅ Verification

After deployment completes:

1. **Check Backend Health:**
   ```
   https://your-backend-url.onrender.com/docs
   ```
   You should see the API documentation.

2. **Check Frontend:**
   ```
   https://your-frontend-url.vercel.app
   ```
   The app should load.

3. **Test Full Flow:**
   - Upload a resume
   - Enter job description
   - Click "Analyze" → Should show ATS score
   - Click "Enhance" → Should work!

---

## 🔧 Troubleshooting

### Build Still Fails

If you still get PyMuPDF errors:

**Try even older version:**

Edit `requirements-render.txt`:
```python
PyMuPDF==1.22.5  # Even older stable version
```

Then:
```bash
git add backend/requirements-render.txt
git commit -m "Use older PyMuPDF version"
git push origin main
```

Render will auto-redeploy.

### Backend Crashes on Startup

**Check Logs:**
1. Render Dashboard → Your Service → Logs
2. Look for specific error messages

**Common Issues:**
- Missing environment variable → Add it in Render Environment tab
- Import error → Package version conflict
- Port error → Make sure start command uses `$PORT`

### AI Enhancement Not Working

1. **Verify API Key:**
   - Render Dashboard → Environment → Check `GEMINI_API_KEY`
   - Test at: https://aistudio.google.com

2. **Check Logs:**
   - Look for "503" or "429" errors
   - If 503: Google's servers are overloaded (temporary)
   - If 429: Rate limit hit (wait 60 seconds)

### CORS Errors

**Frontend can't connect to backend:**

1. **Check FRONTEND_ORIGIN in backend environment**
2. Must match your Vercel URL exactly
3. No trailing slash!
   ```
   ✅ Correct: https://resumeforge.vercel.app
   ❌ Wrong: https://resumeforge.vercel.app/
   ```

---

## 📊 What Changed

### Files Modified:

1. **requirements.txt** → Downgraded PyMuPDF to 1.23.26
2. **requirements-render.txt** → Special file for Render with stable versions
3. **render.yaml** → Blueprint for one-click Render deployment
4. **backend/runtime.txt** → Specify Python 3.11

### Why These Changes?

- **PyMuPDF 1.24.x** tries to compile from source → fails on Render
- **PyMuPDF 1.23.8** has pre-built binary wheels → works on Render
- **Removed hiredis** → Optional Redis optimization, not needed
- **Older reportlab** → More stable, has binary wheels

---

## 🎯 Alternative: Use Docker on Render

If you still have issues, deploy with Docker instead:

1. **Render Dashboard** → **New** → **Web Service**
2. **Docker** tab
3. **Dockerfile Path:** `backend/Dockerfile`
4. Add environment variables
5. Deploy

Docker builds everything from scratch and usually works better!

---

## 💰 Cost

**Render Free Tier:**
- ✅ Free for 750 hours/month
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Takes 30-60 seconds to wake up (first request)

**Render Starter ($7/month):**
- ✅ Always on
- ✅ Faster builds
- ✅ More resources

---

## 🆘 Still Having Issues?

1. **Check Render Status:** https://status.render.com
2. **Render Docs:** https://render.com/docs
3. **Our Full Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)
4. **Open GitHub Issue** with:
   - Full error message
   - Render build logs
   - Your requirements file

---

## ✨ Success!

Once deployed:
- ✅ Backend: https://your-app.onrender.com
- ✅ Frontend: https://your-app.vercel.app
- ✅ API Docs: https://your-app.onrender.com/docs

**🎉 Your ResumeForge AI is live!**
