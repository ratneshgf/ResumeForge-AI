# Quick Deployment Guide

Choose your deployment method:

## 🚀 Fastest: Vercel + Render (5 minutes)

**Free tier, no credit card required**

### 1. Deploy Backend (Render)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Click button above → Sign up/Login
2. New → Web Service → Connect GitHub
3. Settings:
   - Name: `resumeforge-backend`
   - Root: `backend`
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   ```
   GEMINI_API_KEY=your_key_here
   AI_PROVIDER=gemini
   AI_MAX_RETRIES=5
   AI_TIMEOUT_SECONDS=90
   ```
5. Deploy → Copy URL

### 2. Deploy Frontend (Vercel)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Click button → Sign up/Login
2. Import GitHub repo
3. Settings:
   - Root: `frontend`
   - Framework: Vite
4. Environment Variable:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```
5. Deploy → Done!

### 3. Update CORS

Back to Render → Backend → Environment:
```
FRONTEND_ORIGIN=https://your-frontend-url.vercel.app
```
Save & Redeploy.

---

## 🐳 Docker (One Command)

**Best for VPS/Cloud deployment**

```bash
# 1. Clone repository
git clone https://github.com/yourusername/resumeforge-project.git
cd resumeforge-project

# 2. Configure environment
cp backend/.env.example .env
nano .env  # Add your GEMINI_API_KEY

# 3. Deploy
docker-compose up -d --build

# ✅ Done! Access at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
```

---

## 🛠️ Manual Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📋 Required API Keys

### Gemini API (Free)
1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy key → Add to `.env` as `GEMINI_API_KEY`

### Razorpay (Optional - for payments)
1. Go to: https://dashboard.razorpay.com
2. Sign up → Get Test Keys
3. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=rzp_test_xxx
   RAZORPAY_KEY_SECRET=xxx
   ```

---

## 🔍 Troubleshooting

### "Failed to fetch" error
→ Check CORS: `FRONTEND_ORIGIN` in backend must match frontend URL

### AI enhancement not working
→ Verify `GEMINI_API_KEY` is set correctly in environment variables

### Docker build fails
→ Ensure you have enough disk space (need ~2GB)

---

## 📚 Full Documentation

For detailed deployment guides:
- **Full Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Main README:** [README.md](./README.md)

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
ENV=production
FRONTEND_ORIGIN=https://your-frontend-url.com
GEMINI_API_KEY=your_actual_key
AI_PROVIDER=gemini
AI_MAX_RETRIES=5
AI_TIMEOUT_SECONDS=90
AI_TEMPERATURE=0.7
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
USE_REDIS=false
MAX_UPLOAD_MB=5
FILE_TTL_MINUTES=60
RATE_LIMIT_PER_MINUTE=30
LOG_LEVEL=INFO
```

#### Frontend (.env.local)
```env
VITE_API_URL=https://your-backend-url.com
```

---

## 🚨 Security Checklist

Before deploying to production:

- [ ] Change all default API keys
- [ ] Set strong `RAZORPAY_KEY_SECRET`
- [ ] Enable HTTPS (auto with Vercel/Render)
- [ ] Set correct `FRONTEND_ORIGIN` for CORS
- [ ] Review rate limits
- [ ] Enable Redis for production (`USE_REDIS=true`)
- [ ] Set up error monitoring (Sentry)
- [ ] Regular backups

---

## 📊 Monitoring

### Check Health
```bash
# Backend health
curl https://your-backend-url.com/api/v1/health

# View logs (Docker)
docker-compose logs -f

# View logs (Render/Vercel)
Check dashboard
```

---

## 🆘 Need Help?

- **Issues:** Open GitHub issue
- **Email:** support@resumeforge.com
- **Docs:** Full deployment guide in [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**🎉 Happy Deploying!**
