# 📋 Pre-Deployment Checklist

Use this checklist before deploying to ensure everything is ready.

## ✅ Step 1: Local Testing

Test everything locally first:

- [ ] Backend starts without errors: `cd backend && uvicorn app.main:app --reload`
- [ ] Frontend starts without errors: `cd frontend && npm run dev`
- [ ] Can upload a resume (PDF file)
- [ ] ATS analysis works and shows score
- [ ] AI enhancement works (most critical!)
- [ ] Can download enhanced PDF
- [ ] No errors in browser console
- [ ] No errors in backend terminal

## ✅ Step 2: API Keys

Get and verify your API keys:

### Gemini API Key (Required)
- [ ] Go to: https://aistudio.google.com/apikey
- [ ] Create API key
- [ ] Copy key (starts with `AQ.`)
- [ ] Test it works: `python backend/test_models.py`
- [ ] Verify quota is available

### Razorpay (Optional - for payments)
- [ ] Sign up at: https://dashboard.razorpay.com
- [ ] Get Test/Live keys
- [ ] Copy Key ID and Secret
- [ ] Save for later

## ✅ Step 3: Code Preparation

Prepare your code for deployment:

- [ ] Commit all changes: `git add . && git commit -m "Ready for deployment"`
- [ ] Push to GitHub: `git push origin main`
- [ ] No sensitive data in code (API keys, passwords)
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` has no real keys
- [ ] All dependencies listed in `requirements.txt` and `package.json`

## ✅ Step 4: Environment Configuration

Set up your environment files:

### Backend (.env)
- [ ] Copy from example: `cp backend/.env.example backend/.env`
- [ ] Set `GEMINI_API_KEY=your_actual_key`
- [ ] Set `AI_MAX_RETRIES=5`
- [ ] Set `AI_TIMEOUT_SECONDS=90`
- [ ] Set `ENV=production` (for production)
- [ ] Update `FRONTEND_ORIGIN` when you know frontend URL
- [ ] Add Razorpay keys if using payments

### Frontend (.env.local)
- [ ] Create file: `touch frontend/.env.local`
- [ ] Add: `VITE_API_URL=your_backend_url`
- [ ] Will update after backend is deployed

## ✅ Step 5: Choose Deployment Platform

Select ONE option:

### Option A: Vercel + Render (Recommended for beginners)
- [ ] Render account created
- [ ] Vercel account created
- [ ] GitHub connected to both
- [ ] Ready to follow [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)

### Option B: Docker (VPS/Cloud)
- [ ] Docker installed: `docker --version`
- [ ] Docker Compose installed: `docker-compose --version`
- [ ] Server/VPS ready (min 1GB RAM)
- [ ] SSH access configured
- [ ] Ready to follow Docker section in [DEPLOYMENT.md](./DEPLOYMENT.md)

### Option C: Railway
- [ ] Railway account created
- [ ] GitHub connected
- [ ] Ready to follow Railway section

### Option D: Manual VPS
- [ ] VPS provisioned (Ubuntu 22.04+)
- [ ] SSH access working
- [ ] Domain name ready (optional)
- [ ] Ready to follow Manual VPS section

## ✅ Step 6: Security Review

Before going live:

- [ ] All API keys are in environment variables (not in code)
- [ ] `.env` file is in `.gitignore`
- [ ] No console.log with sensitive data
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] File upload limits set (`MAX_UPLOAD_MB=5`)
- [ ] HTTPS will be enabled (automatic with Vercel/Render)

## ✅ Step 7: Performance Settings

Optimize for production:

- [ ] `AI_MAX_RETRIES=5` (handle API issues)
- [ ] `AI_TIMEOUT_SECONDS=90` (long enough for Gemini)
- [ ] `RATE_LIMIT_PER_MINUTE=30` (prevent abuse)
- [ ] `FILE_TTL_MINUTES=60` (auto-cleanup uploads)
- [ ] `LOG_LEVEL=INFO` (production logging)

## ✅ Step 8: Deployment Execution

Follow your chosen guide:

- [ ] Backend deployed successfully
- [ ] Backend URL copied
- [ ] Frontend environment updated with backend URL
- [ ] Frontend deployed successfully
- [ ] Frontend URL copied
- [ ] Backend CORS updated with frontend URL
- [ ] Both services restarted/redeployed

## ✅ Step 9: Post-Deployment Testing

Test your live application:

- [ ] Frontend loads at your URL
- [ ] Backend /docs loads (add `/docs` to backend URL)
- [ ] Upload resume works
- [ ] ATS analysis works
- [ ] AI enhancement works (critical!)
- [ ] Download PDF works
- [ ] No console errors
- [ ] No CORS errors
- [ ] All features work on mobile

## ✅ Step 10: Monitoring Setup

Set up monitoring (optional but recommended):

- [ ] Error tracking (Sentry, Rollbar)
- [ ] Uptime monitoring (UptimeRobot, Pingdom)
- [ ] Log aggregation (Papertrail, Loggly)
- [ ] Performance monitoring (New Relic, DataDog)
- [ ] Set up alerts for errors

## ✅ Step 11: Documentation

Document your deployment:

- [ ] Save backend URL
- [ ] Save frontend URL
- [ ] Document environment variables used
- [ ] Save deployment credentials (securely!)
- [ ] Create backup of .env file (encrypted/secure)
- [ ] Document any custom configurations

## ✅ Step 12: Final Checks

Before announcing:

- [ ] Test from different devices (phone, tablet, desktop)
- [ ] Test from different browsers (Chrome, Firefox, Safari)
- [ ] Test from different locations (ask friends)
- [ ] Load test with multiple uploads
- [ ] Verify AI enhancement doesn't hit rate limits
- [ ] Check logs for any errors
- [ ] Verify SSL certificate (HTTPS padlock)

---

## 🚨 Critical Items (Must Have)

These MUST work before going live:

1. ✅ **Resume Upload** - Core feature
2. ✅ **ATS Scoring** - Core feature  
3. ✅ **AI Enhancement** - MOST IMPORTANT!
4. ✅ **PDF Download** - Core feature
5. ✅ **HTTPS Enabled** - Security requirement
6. ✅ **CORS Configured** - Prevents errors
7. ✅ **No API Key Leaks** - Security requirement

---

## 📊 Success Metrics

Your deployment is successful when:

- [ ] Uptime > 99.5%
- [ ] AI enhancement success rate > 95%
- [ ] Average response time < 3 seconds
- [ ] No security vulnerabilities
- [ ] Zero data leaks
- [ ] Users can complete full workflow

---

## 🆘 Emergency Rollback

If something goes wrong:

### Vercel
```bash
# Rollback to previous deployment
# Vercel Dashboard → Deployments → Previous version → Promote to Production
```

### Render
```bash
# Render Dashboard → Service → Manual Deploy → Select previous commit
```

### Docker
```bash
# Stop and remove
docker-compose down

# Pull previous version
git checkout <previous-commit>

# Restart
docker-compose up -d --build
```

---

## 📞 Support Contacts

Save these for deployment day:

- **Vercel Support:** https://vercel.com/support
- **Render Support:** https://render.com/support  
- **Docker Issues:** https://docs.docker.com
- **Gemini API Status:** https://status.cloud.google.com

---

## 🎯 Deployment Day Timeline

Recommended schedule:

1. **Morning:** Deploy backend → Test
2. **Afternoon:** Deploy frontend → Test
3. **Evening:** Final testing → Monitor
4. **Next Day:** Announce if stable

**Don't rush! Better to deploy slowly and correctly.**

---

## ✨ Post-Launch Tasks

After successful deployment:

- [ ] Announce on social media
- [ ] Add to portfolio
- [ ] Share with friends/colleagues
- [ ] Collect feedback
- [ ] Monitor for issues
- [ ] Plan improvements
- [ ] Celebrate! 🎉

---

**Ready to deploy? Pick your platform and follow the guide!**

- 🚀 [Quick Deploy Guide](./QUICK_DEPLOY.md)
- 📚 [Full Deployment Guide](./DEPLOYMENT.md)
- 📊 [Deployment Summary](./DEPLOYMENT_SUMMARY.md)
