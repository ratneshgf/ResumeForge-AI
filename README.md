# ResumeForge AI

**Production-grade AI-powered resume optimization with template preservation.**

Upload your resume + target job description → get back an AI-optimized version with the **same design and formatting**.

## 🎯 What Makes This Different

- ✅ **True Template Preservation** - Keeps your original fonts, colors, layout . 
- ✅ **Real AI Enhancement** - Google Gemini/OpenAI powered content optimization
- ✅ **Production ATS Scoring** - Multi-technique NLP (30-95% realistic range)
- ✅ **Comprehensive Skill Matching** - 1000+ skills vs 25 hardcoded
- ✅ **Secure Payment Integration** - Razorpay with webhook verification
- ✅ **No Mock Responses** - Every feature uses real AI and NLP

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- **Gemini or OpenAI API key** (required for AI features)

### Backend Setup

```bash
cd backend

# Install dependencies
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Download required NLP models
python -m spacy download en_core_web_md
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Configure environment
cp .env.example .env
# IMPORTANT: Edit .env and add your GEMINI_API_KEY or OPENAI_API_KEY

# Create storage directories
mkdir -p storage/uploads storage/temp storage/output

# Run backend
uvicorn app.main:app --reload
```

Backend runs at **http://localhost:8000**  
Interactive API docs at **http://localhost:8000/docs**

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:5173**

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and deployment guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[CHANGES_EXPLAINED.md](CHANGES_EXPLAINED.md)** - Prototype → Production transformation

---

## 🔑 Getting API Keys

### Google Gemini (Recommended)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API Key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`
4. **Free tier:** 60 requests/minute

### OpenAI (Alternative)
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create API Key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`
4. **Paid:** ~$0.002 per 1K tokens

---

## ✨ Features

### Production-Ready Features

✅ **Real ATS Scoring** (not fake 95-100%)
- Sentence Transformers for semantic similarity (25%)
- TF-IDF keyword extraction (20%)
- 1000+ skill taxonomy matching (25%)
- Experience level analysis (15%)
- Education matching (10%)
- Completeness checks (5%)

✅ **AI Resume Enhancement**
- Real Gemini/OpenAI integration
- Section-specific strategies (objective, skills, experience)
- Preserves factual accuracy
- Protected sections never modified

✅ **Template Preservation**
- DOCX: True in-place editing with formatting
- PDF: Enhanced rendering with style preservation
- Multi-run paragraph handling

✅ **Security**
- Payment signature verification (HMAC-SHA256)
- Webhook signature verification
- File magic byte validation
- Rate limiting
- Comprehensive error handling

### User Flow

1. **Upload** → Resume (DOCX/PDF) + Job Description
2. **Analyze** → Real ATS score with detailed breakdown
3. **Enhance** → AI optimizes content for target job
4. **Compare** → Review before/after changes
5. **Download** → Get optimized resume in original format

---

## 🏗️ Technical Stack

### Backend
- FastAPI (Python 3.9+)
- spaCy (NLP - en_core_web_md)
- Sentence Transformers (Semantic similarity)
- scikit-learn (TF-IDF, ML)
- NLTK (Tokenization)
- python-docx, PyMuPDF, ReportLab
- Razorpay (Payments)

### Frontend
- React 18 + TypeScript
- TailwindCSS
- Vite
- React Router
- TanStack Query

### AI Providers
- Google Gemini 1.5 Flash (Primary)
- OpenAI GPT-4o-mini (Alternative)

---

## 📊 What Changed from Prototype

| Feature | Before (Prototype) | After (Production) |
|---------|-------------------|-------------------|
| **ATS Scoring** | 25 hardcoded skills, 95-100% for all | 1000+ skills, 30-95% realistic |
| **AI Enhancement** | Mock responses, returned original text | Real AI with retries and validation |
| **Error Handling** | Silent failure | Explicit errors with retry logic |
| **Payment Security** | No webhook verification | HMAC-SHA256 signature verification |
| **Section Detection** | 8 keywords | 50+ keywords, multi-heuristic |
| **Skill Extraction** | String matching | NLP + comprehensive taxonomy |
| **JD Analysis** | Hardcoded fallback | AI + intelligent extraction |

See [CHANGES_EXPLAINED.md](CHANGES_EXPLAINED.md) for complete details.

---

## 🔐 Security

- ✅ File magic byte validation
- ✅ Size limits (5MB default)
- ✅ Rate limiting (30 req/min)
- ✅ Payment signature verification
- ✅ Webhook signature verification
- ✅ Idempotency checks
- ✅ Structured logging
- ✅ No silent error degradation

---

## 🌍 Deployment

### Required Environment Variables

```bash
# AI Provider (REQUIRED)
GEMINI_API_KEY=your_key  # or OPENAI_API_KEY

# Payment (for monetization)
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret

# CORS
FRONTEND_ORIGIN=https://your-domain.com
```

### Recommended Platforms

- **Backend:** Railway, Heroku, Google Cloud Run, AWS Elastic Beanstalk
- **Frontend:** Vercel, Netlify, CloudFlare Pages
- **Redis:** Redis Labs (free 30MB), AWS ElastiCache

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

---

## 🧪 Testing

### Manual Testing Checklist

```bash
# 1. Test health endpoint
curl http://localhost:8000/health

# 2. Upload resume
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -F "file=@resume.docx"

# 3. Test JD analysis
curl -X POST http://localhost:8000/api/v1/jd/analyze \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "job_description": "Python developer..."}'
```

### Verify Different Resumes Get Different Scores

Upload multiple resumes with varying experience levels - they should receive different, realistic ATS scores (not all 95-100%).

---

## 📈 Performance

### Optimizations
- Lazy loading of NLP models
- Global model caching
- Async background tasks
- Efficient file streaming

### For Scale (TODO)
- Redis session store
- Celery/RQ task queue
- CDN for static assets
- Database for user accounts

---

## 🐛 Known Limitations

1. **PDF Template Preservation** - Better than before, but not perfect (PDF limitation)
2. **Session Store** - In-memory (enable Redis for multi-worker: `USE_REDIS=true`)
3. **Rate Limiting** - In-memory (use Redis-backed for distributed)

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅ (COMPLETE)
- [x] Real ATS scoring with NLP
- [x] AI enhancement with Gemini/OpenAI
- [x] Template preservation
- [x] Secure payment integration
- [x] Production error handling

### Phase 2: Scale & Enhancement
- [ ] Redis session store
- [ ] Database integration
- [ ] User accounts
- [ ] Resume version history
- [ ] Async task queue

### Phase 3: Advanced Features
- [ ] Cover letter generator
- [ ] Interview question generator
- [ ] Template marketplace
- [ ] LinkedIn import
- [ ] Mobile app

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

Built with:
- spaCy - Industrial NLP
- Sentence Transformers - Semantic similarity
- python-docx - Document manipulation
- FastAPI - Modern Python framework
- React - UI library

---

## 📞 Support

- **API Docs:** http://localhost:8000/docs
- **Issues:** GitHub Issues
- **Setup Help:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Status:** Production Ready ✅  
**Version:** 2.0.0  
**Last Updated:** 2024

**Built with ❤️ for job seekers worldwide** 🌍📄✨
