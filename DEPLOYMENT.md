# ResumeForge AI - Deployment Guide

This guide covers multiple deployment options for ResumeForge AI project.

## Table of Contents
1. [Quick Deploy (Vercel + Render)](#option-1-vercel--render-free--easiest)
2. [Docker Compose (Self-Hosted)](#option-2-docker-compose-self-hosted)
3. [Railway (All-in-One)](#option-3-railway-all-in-one)
4. [Manual VPS Deployment](#option-4-manual-vps-deployment)

---

## Prerequisites

Before deploying, ensure you have:
- ✅ Gemini API Key (from https://aistudio.google.com/apikey)
- ✅ Git installed
- ✅ GitHub account (for Vercel/Railway deployment)

---

## Option 1: Vercel + Render (Free & Easiest)

**Best for:** Quick deployment, free hosting, no server management

### Step 1: Deploy Backend to Render

1. **Go to [Render.com](https://render.com)** and sign up/login

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository**

4. **Configure the service:**
   - **Name:** `resumeforge-backend`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables:**
   ```
   ENV=production
   GEMINI_API_KEY=your_actual_gemini_api_key
   AI_PROVIDER=gemini
   AI_MAX_RETRIES=5
   AI_TIMEOUT_SECONDS=90
   AI_TEMPERATURE=0.7
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   USE_REDIS=false
   MAX_UPLOAD_MB=5
   FILE_TTL_MINUTES=60
   RATE_LIMIT_PER_MINUTE=30
   LOG_LEVEL=INFO
   ```

6. **Click "Create Web Service"**

7. **Copy your backend URL** (e.g., `https://resumeforge-backend.onrender.com`)

### Step 2: Deploy Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com)** and sign up/login

2. **Click "Add New" → "Project"**

3. **Import your GitHub repository**

4. **Configure the project:**
   - **Framework Preset:** `Vite`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

5. **Add Environment Variable:**
   ```
   VITE_API_URL=https://resumeforge-backend.onrender.com
   ```
   *(Replace with your actual Render backend URL)*

6. **Click "Deploy"**

7. **Copy your frontend URL** (e.g., `https://resumeforge.vercel.app`)

### Step 3: Update CORS

Go back to **Render dashboard** → Your backend service → **Environment**:

Add/Update:
```
FRONTEND_ORIGIN=https://resumeforge.vercel.app
```
*(Replace with your actual Vercel frontend URL)*

**Save and redeploy** the backend.

### ✅ Done! Your app is live!

---

## Option 2: Docker Compose (Self-Hosted)

**Best for:** VPS deployment, full control, single-command setup

### Prerequisites
- Docker & Docker Compose installed
- Server with at least 1GB RAM

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/resumeforge-project.git
cd resumeforge-project
```

### Step 2: Configure Environment

Create a `.env` file in the project root:

```bash
# Copy from backend example
cp backend/.env.example .env
```

Edit `.env` and add your actual API keys:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### Step 3: Build and Start

```bash
# Build and start all services
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Step 4: Access Your Application

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Useful Commands

```bash
# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose up -d --build

# Clean up everything
docker-compose down -v
```

### Production Tips

1. **Use a reverse proxy (Nginx/Caddy) for HTTPS:**
   ```bash
   # Install Caddy
   sudo apt install caddy
   
   # Edit Caddyfile
   sudo nano /etc/caddy/Caddyfile
   ```
   
   Add:
   ```
   resumeforge.yourdomain.com {
       reverse_proxy localhost:3000
   }
   
   api.resumeforge.yourdomain.com {
       reverse_proxy localhost:8000
   }
   ```

2. **Set up automatic backups for uploads:**
   ```bash
   # Backup storage volume
   docker run --rm -v resumeforge_storage:/data -v $(pwd):/backup alpine tar czf /backup/storage-backup.tar.gz /data
   ```

---

## Option 3: Railway (All-in-One)

**Best for:** Simple deployment, good free tier, automatic HTTPS

### Step 1: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)** and sign up/login

2. **Click "New Project" → "Deploy from GitHub repo"**

3. **Select your repository**

### Step 2: Add Backend Service

1. **Click "Add Service" → "GitHub Repo"**
2. **Configure:**
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables** (same as Render above)

4. **Generate Domain** → Copy the URL

### Step 3: Add Frontend Service

1. **Click "Add Service" → "GitHub Repo"** (same repo)
2. **Configure:**
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npx serve -s dist -l $PORT`

3. **Add Environment Variable:**
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

4. **Generate Domain** → Copy the URL

### Step 4: Update Backend CORS

Go to backend service → Environment Variables:
```
FRONTEND_ORIGIN=https://your-frontend-url.railway.app
```

**Redeploy** both services.

---

## Option 4: Manual VPS Deployment

**Best for:** Full control, custom domain, learning

### Prerequisites
- VPS with Ubuntu 22.04+ (DigitalOcean, AWS, Linode, etc.)
- Domain name (optional but recommended)

### Step 1: Initial Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3.11 python3-pip nodejs npm nginx certbot python3-certbot-nginx git

# Create app user
adduser resumeforge
usermod -aG sudo resumeforge
su - resumeforge
```

### Step 2: Clone and Setup Backend

```bash
# Clone repository
git clone https://github.com/yourusername/resumeforge-project.git
cd resumeforge-project/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Test the app
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 3: Setup Backend as Service

Create systemd service:

```bash
sudo nano /etc/systemd/system/resumeforge-backend.service
```

Add:
```ini
[Unit]
Description=ResumeForge Backend
After=network.target

[Service]
Type=simple
User=resumeforge
WorkingDirectory=/home/resumeforge/resumeforge-project/backend
Environment="PATH=/home/resumeforge/resumeforge-project/backend/venv/bin"
ExecStart=/home/resumeforge/resumeforge-project/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable resumeforge-backend
sudo systemctl start resumeforge-backend
sudo systemctl status resumeforge-backend
```

### Step 4: Setup Frontend

```bash
cd ~/resumeforge-project/frontend

# Install dependencies
npm install

# Create production build
npm run build

# Copy to nginx directory
sudo cp -r dist/* /var/www/resumeforge/
```

### Step 5: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/resumeforge
```

Add:
```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    root /var/www/resumeforge;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/resumeforge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Setup SSL with Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

### Step 7: Setup Automatic Renewals

```bash
# Test renewal
sudo certbot renew --dry-run

# Renewal happens automatically via cron
```

---

## Post-Deployment Checklist

After deployment, verify:

- [ ] Frontend loads without errors
- [ ] Backend API responds at `/docs`
- [ ] Resume upload works
- [ ] ATS scoring works
- [ ] AI enhancement works
- [ ] PDF generation works
- [ ] HTTPS is enabled (production)
- [ ] Environment variables are set correctly
- [ ] CORS is configured properly

## Monitoring & Logs

### Render
- Dashboard → Service → Logs

### Vercel
- Dashboard → Project → Deployments → View Function Logs

### Docker Compose
```bash
docker-compose logs -f
```

### Systemd (VPS)
```bash
sudo journalctl -u resumeforge-backend -f
```

---

## Troubleshooting

### Backend not starting
```bash
# Check logs
docker-compose logs backend

# Verify environment variables
docker-compose exec backend env

# Test locally
cd backend
python -m uvicorn app.main:app --reload
```

### Frontend can't connect to backend
1. Check `VITE_API_URL` environment variable
2. Verify CORS settings in backend
3. Check browser console for errors

### AI enhancement failing
1. Verify Gemini API key is set correctly
2. Check API quota at https://aistudio.google.com
3. Review backend logs for specific errors

---

## Scaling Considerations

### For High Traffic:

1. **Enable Redis for session storage**
2. **Use a CDN** (Cloudflare, AWS CloudFront)
3. **Add load balancer** for multiple backend instances
4. **Use object storage** (S3, Cloudflare R2) for file uploads
5. **Add caching layer** (Redis, Memcached)
6. **Monitor with** Sentry, LogRocket, or New Relic

---

## Cost Estimates

### Free Tier (Render + Vercel)
- **Cost:** $0/month
- **Good for:** Testing, small projects, demos

### Railway Hobby
- **Cost:** $5-20/month
- **Good for:** Small to medium apps

### VPS (DigitalOcean, Linode)
- **Cost:** $5-10/month (basic droplet)
- **Good for:** Full control, custom setup

### Production Ready (AWS/GCP)
- **Cost:** $50-200/month
- **Includes:** Load balancer, auto-scaling, monitoring

---

## Security Best Practices

1. **Never commit `.env` files**
2. **Use strong API keys**
3. **Enable rate limiting**
4. **Keep dependencies updated**
5. **Regular backups**
6. **Monitor logs for suspicious activity**
7. **Use HTTPS everywhere**
8. **Implement proper CORS**
9. **Sanitize file uploads**
10. **Set up error tracking** (Sentry)

---

## Need Help?

- **Issues:** Open a GitHub issue
- **Documentation:** Check README.md
- **Community:** Join Discord/Slack (if available)

---

**Happy Deploying! 🚀**
