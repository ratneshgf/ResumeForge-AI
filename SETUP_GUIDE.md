# ResumeForge AI - Production Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- Redis (optional, for production scaling)
- Gemini or OpenAI API key
- Razorpay account (for payments)

---

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Download NLP Models

```bash
# Download spaCy model (required for ATS scoring)
python -m spacy download en_core_web_md

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
```

**Required Configuration:**

```bash
# AI Provider (choose one)
GEMINI_API_KEY=your_gemini_key_here
# OR
OPENAI_API_KEY=your_openai_key_here

AI_PROVIDER=gemini  # or "openai"
```

**Optional but Recommended:**

```bash
# Payment (for monetization)
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret

# Redis (for scaling beyond single process)
USE_REDIS=true
REDIS_URL=redis://localhost:6379/0

# Security
FRONTEND_ORIGIN=https://your-domain.com  # In production
```

### 4. Create Storage Directories

```bash
mkdir -p storage/uploads storage/temp storage/output
```

### 5. Run Backend

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Backend will run at `http://localhost:8000`

API docs at `http://localhost:8000/docs`

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# For production
echo "VITE_API_URL=https://api.your-domain.com" > .env
```

### 3. Run Frontend

```bash
# Development
npm run dev

# Production build
npm run build
```

Frontend will run at `http://localhost:5173`

---

## Getting API Keys

### Google Gemini API (Recommended)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

**Free Tier:** 60 requests per minute

### OpenAI API (Alternative)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key to your `.env` file

**Pricing:** Pay per token (~$0.002 per 1K tokens for gpt-4o-mini)

### Razorpay (For Payments)

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up for account
3. Complete KYC verification
4. Go to Settings → API Keys
5. Generate Test/Live keys
6. Copy Key ID and Secret to your `.env` file

---

## Redis Setup (Optional, for Production)

### Local Redis (Development)

**Windows:**
```bash
# Download from https://github.com/microsoftarchive/redis/releases
# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Mac:**
```bash
brew install redis
brew services start redis
```

### Configure Backend to Use Redis

```bash
# In backend/.env
USE_REDIS=true
REDIS_URL=redis://localhost:6379/0
```

### Cloud Redis (Production)

**Options:**
- Redis Labs (Free 30MB)
- AWS ElastiCache
- Google Cloud Memorystore
- Azure Cache for Redis

---

## Verification Steps

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "app": "ResumeForge AI",
  "version": "2.0.0",
  "environment": "development"
}
```

### 2. Test AI Integration

```bash
curl -X POST http://localhost:8000/api/v1/jd/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "job_description": "We are looking for a Python developer with 3+ years of experience in Django and React."
  }'
```

Should return extracted skills and requirements.

### 3. Test File Upload

```bash
# Prepare a test DOCX resume
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -F "file=@path/to/resume.docx"
```

Should return parsed resume sections.

### 4. Test Frontend

Navigate to `http://localhost:5173` and verify:
- Landing page loads
- Upload page accepts files
- No console errors

---

## Common Issues and Solutions

### Issue: "spaCy model not found"

**Solution:**
```bash
python -m spacy download en_core_web_md
```

### Issue: "AI API key not configured"

**Solution:**
Check `.env` file has valid `GEMINI_API_KEY` or `OPENAI_API_KEY`

### Issue: "Module not found: sentence-transformers"

**Solution:**
```bash
pip install sentence-transformers
```

### Issue: "NLTK data not found"

**Solution:**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Issue: "Redis connection failed"

**Solution:**
Either:
1. Start Redis: `redis-server`
2. Or disable Redis: `USE_REDIS=false` in `.env`

### Issue: "Port already in use"

**Solution:**
```bash
# Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Issue: "CORS error in browser"

**Solution:**
Check `FRONTEND_ORIGIN` in backend `.env` matches frontend URL

---

## Production Deployment

### Environment Variables Checklist

```bash
# Required
✓ GEMINI_API_KEY or OPENAI_API_KEY
✓ RAZORPAY_KEY_ID (for payments)
✓ RAZORPAY_KEY_SECRET (for payments)
✓ FRONTEND_ORIGIN (your frontend domain)

# Recommended
✓ ENV=production
✓ USE_REDIS=true
✓ REDIS_URL=redis://your-redis-url
✓ LOG_LEVEL=INFO
```

### Deployment Platforms

#### Heroku

```bash
# Backend
heroku create your-app-name
heroku addons:create heroku-redis:mini
heroku config:set GEMINI_API_KEY=your_key
git push heroku main

# Frontend (separate app or use Vercel)
```

#### Railway.app

1. Connect GitHub repo
2. Add environment variables
3. Deploy automatically on push

#### AWS (Elastic Beanstalk)

```bash
eb init
eb create production
eb deploy
```

#### DigitalOcean App Platform

1. Connect GitHub repo
2. Configure build settings
3. Add environment variables
4. Deploy

#### Google Cloud Run

```bash
gcloud run deploy resumeforge \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend Deployment

#### Vercel (Recommended)

```bash
cd frontend
npm install -g vercel
vercel
```

#### Netlify

```bash
cd frontend
npm run build
# Drag-drop `dist` folder to Netlify
```

#### CloudFlare Pages

```bash
cd frontend
npm run build
# Connect repo and deploy
```

---

## Performance Optimization

### 1. Enable Caching

TODO: Implement Redis caching for:
- JD analysis results
- Skill taxonomy lookups
- AI responses (with cache invalidation)

### 2. Async Processing

TODO: Use Celery or RQ for:
- Resume enhancement
- Document generation
- Email notifications

### 3. CDN for Frontend

Use CloudFlare, AWS CloudFront, or similar for:
- Static assets
- Faster global delivery
- DDoS protection

### 4. Database Connection Pooling

When adding database:
- Use connection pooling (SQLAlchemy, Django ORM)
- Set appropriate pool size
- Enable connection recycling

### 5. Load Balancing

For high traffic:
- Multiple backend instances
- Nginx/HAProxy load balancer
- Sticky sessions if not using Redis

---

## Monitoring Setup

### Application Monitoring

**Sentry (Error Tracking):**
```bash
pip install sentry-sdk[fastapi]
```

```python
# In app/main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

**Prometheus (Metrics):**
```bash
pip install prometheus-fastapi-instrumentator
```

**Datadog/New Relic:**
Follow platform-specific integration guides

### Health Checks

Configure platform health check endpoints:
- `/health` - Basic health check
- `/api/v1/resume/upload` - Check if API is responsive

### Log Aggregation

**Options:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- Datadog Logs
- CloudWatch Logs (AWS)
- Google Cloud Logging

---

## Security Best Practices

### 1. Environment Variables

- Never commit `.env` files
- Use secrets management (AWS Secrets Manager, Vault)
- Rotate API keys regularly

### 2. HTTPS

```bash
# Get free SSL certificate
sudo certbot --nginx -d your-domain.com
```

### 3. Rate Limiting

Already implemented in code. Configure:
```bash
RATE_LIMIT_PER_MINUTE=30  # Adjust based on needs
```

### 4. Input Validation

Already implemented:
- File type validation (magic bytes)
- File size limits
- JSON schema validation

### 5. CORS

Configure properly:
```bash
FRONTEND_ORIGIN=https://your-exact-domain.com
```

### 6. Payment Security

- Webhook signature verification: ✓ Implemented
- HTTPS only for payment endpoints
- Never log sensitive payment data

---

## Backup Strategy

### What to Backup

1. **Database** (when implemented)
   - User accounts
   - Payment records
   - Resume metadata

2. **Uploaded Files**
   - Original resumes
   - Generated documents
   - Use S3 versioning

3. **Configuration**
   - `.env` files (securely)
   - Infrastructure as Code

### Backup Schedule

- **Database:** Hourly incremental, daily full
- **Files:** Real-time replication (S3)
- **Config:** Version control (Git)

---

## Cost Estimation

### AI API Costs

**Gemini (Recommended):**
- Free tier: 60 requests/min
- Paid: ~$0.00025 per 1K characters

**OpenAI:**
- gpt-4o-mini: ~$0.002 per 1K tokens
- Estimate: $0.01 - $0.05 per resume enhancement

### Infrastructure Costs (Monthly)

**Small Scale** (<1000 users):
- Hosting: $10-20 (Railway, Heroku)
- Redis: Free-$10
- Storage: $5-10
- **Total: ~$25-40/month**

**Medium Scale** (1K-10K users):
- Hosting: $50-100 (multiple instances)
- Redis: $10-30
- Storage: $10-20
- Database: $15-30
- **Total: ~$85-180/month**

**Large Scale** (10K+ users):
- Hosting: $200-500
- Redis: $50-100
- Storage: $50-100
- Database: $50-100
- CDN: $20-50
- **Total: ~$370-850/month**

---

## Testing in Production

### 1. Test Resume Upload

- Upload various formats (DOCX, PDF)
- Try different resume styles
- Test with large files (near limit)

### 2. Test ATS Scoring

- Compare scores across different resumes
- Verify score consistency
- Check detailed breakdown

### 3. Test AI Enhancement

- Review quality of suggestions
- Verify factual accuracy
- Check for hallucinations

### 4. Test Payments (Sandbox)

- Use Razorpay test mode
- Verify webhook delivery
- Test failed payments

### 5. Load Testing

```bash
# Install Apache Bench
apt-get install apache2-utils

# Test upload endpoint
ab -n 100 -c 10 -p resume.docx -T multipart/form-data \
  http://your-domain.com/api/v1/resume/upload
```

---

## Support and Documentation

### For Users

- Create FAQ page
- Video tutorials
- Example before/after resumes
- Live chat support

### For Developers

- API documentation (auto-generated at `/docs`)
- Integration guides
- Webhook examples
- Rate limit information

---

## Next Steps After Setup

1. ✓ Configure API keys
2. ✓ Test all endpoints
3. ✓ Upload test resumes
4. ✓ Review AI enhancement quality
5. ✓ Configure payment gateway
6. ✓ Set up monitoring
7. ✓ Deploy to production
8. ✓ Set up backups
9. ✓ Configure domain and SSL
10. ✓ Launch! 🚀

---

## Getting Help

### Common Resources

- **Documentation:** `/docs` endpoint
- **GitHub Issues:** Report bugs
- **Email Support:** support@your-domain.com
- **Community:** Discord/Slack channel

### Debug Mode

Enable detailed logging:
```bash
LOG_LEVEL=DEBUG
```

Check logs for errors and warnings.

---

**Ready to transform resumes with AI!** 🎯📄✨
