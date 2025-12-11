# 🚀 Deployment Guide - Tarot Místico

**Clean, Production-Ready Deployment to Vercel**

---

## ✅ Pre-Deployment Checklist

All checks passed! Your project is ready for deployment.

### Validation Results
```
✅ Python version: 3.9.24
✅ All required files present
✅ Directory structure correct
✅ vercel.json valid
✅ Python syntax valid
✅ Deployment size: 0.2 MB (within 50 MB limit)
```

---

## 🎯 Quick Deploy (3 Steps)

### Step 1: Login to Vercel
```bash
vercel login
```

### Step 2: Deploy to Production
```bash
vercel --prod
```

### Step 3: Set Environment Variables

In the Vercel Dashboard, add these environment variables:

**Required:**
```
SECRET_KEY=<generate-random-string>
JWT_SECRET_KEY=<generate-random-string>
GEMINI_API_KEY=<your-gemini-api-key>
```

**Optional:**
```
DATABASE_URL=postgresql://...  # Or leave empty for SQLite
FLASK_ENV=production
```

---

## 📁 Clean Project Structure

```
tarot-mistico/
├── api/
│   └── index.py              # Vercel serverless entry (7.1 KB)
├── routes/
│   ├── auth_routes.py        # Authentication
│   ├── user_routes.py        # User management
│   ├── reading_routes.py     # Tarot readings
│   ├── subscription_routes.py # Subscriptions
│   └── astrology_routes.py   # Astrology (optional)
├── src/
│   ├── models.py             # Database models
│   ├── auth.py               # JWT authentication
│   ├── tarot_reader.py       # Tarot logic
│   ├── gemini_service.py     # AI integration
│   └── astrology_calculator.py
├── public/
│   ├── tarot_web.html        # Frontend UI
│   └── tarot_web.js          # Frontend logic
├── .archive/                 # Old builds archived (2.9 MB)
├── app.py                    # Local dev server (4.4 KB)
├── config.py                 # Configuration (2.9 KB)
├── requirements.txt          # Dependencies (904 bytes)
├── vercel.json               # Vercel config (936 bytes)
├── validate.py               # Validation script
├── .env.example              # Environment template
└── README.md                 # Documentation (7.1 KB)
```

---

## 🔧 Vercel Configuration

### vercel.json
```json
{
  "version": 2,
  "name": "tarot-mistico",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/(.*\\.(js|css|png|jpg|...))", "dest": "/public/$1" },
    { "src": "/", "dest": "/public/tarot_web.html" },
    { "src": "/(.*)", "dest": "/public/tarot_web.html" }
  ],
  "functions": {
    "api/index.py": {
      "memory": 1024,
      "maxDuration": 30
    }
  }
}
```

### Key Features
- **Runtime**: Python 3.11
- **Memory**: 1024 MB
- **Timeout**: 30 seconds
- **Region**: US East (iad1)
- **Auto-scaling**: Enabled
- **CDN**: Global edge network

---

## 🧪 Testing Your Deployment

### Health Check
```bash
curl https://your-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Tarot Místico API",
  "version": "2.0.0",
  "platform": "Vercel Serverless",
  "python_version": "3.11.x",
  "routes": {
    "auth": true,
    "user": true,
    "reading": true,
    "subscription": true,
    "astrology": true
  }
}
```

### API Info
```bash
curl https://your-app.vercel.app/api/info
```

### Test Reading
```bash
curl -X POST https://your-app.vercel.app/api/readings/draw \
  -H "Content-Type: application/json" \
  -d '{
    "spread_type": "single",
    "question": "What does today hold for me?"
  }'
```

---

## 🔐 Environment Variables

### Generate Secret Keys

**Option 1: Python**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Option 2: OpenSSL**
```bash
openssl rand -base64 32
```

**Option 3: Online**
Visit: https://randomkeygen.com/

### Set in Vercel

**Via CLI:**
```bash
vercel env add SECRET_KEY
vercel env add JWT_SECRET_KEY
vercel env add GEMINI_API_KEY
```

**Via Dashboard:**
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add each variable for Production environment

---

## 📊 Monitoring

### View Logs
```bash
vercel logs
```

### Real-time Logs
```bash
vercel logs --follow
```

### Deployment Status
```bash
vercel ls
```

---

## 🔄 Continuous Deployment

### Automatic Deployments

Vercel automatically deploys when you push to your repository:

1. **Production**: Push to `main` branch
2. **Preview**: Push to any other branch
3. **Pull Requests**: Automatic preview deployments

### Manual Deployment
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Deploy specific branch
vercel --prod --branch main
```

---

## 🐛 Troubleshooting

### Build Fails

**Check Python version:**
```bash
python3 --version  # Should be 3.9+
```

**Validate locally:**
```bash
python3 validate.py
```

**Check Vercel logs:**
```bash
vercel logs --output
```

### API Errors

**Verify environment variables:**
```bash
vercel env ls
```

**Check function logs:**
```bash
vercel logs api/index.py
```

**Test locally:**
```bash
python3 app.py
```

### Database Issues

**SQLite (default):**
- Automatic, no setup required
- Data persists in `/tmp` (ephemeral)

**PostgreSQL (recommended):**
- Set `DATABASE_URL` environment variable
- Use connection pooling
- Check connection limits

---

## 📈 Performance Optimization

### Current Optimizations
- ✅ Serverless functions (auto-scaling)
- ✅ Global CDN for static assets
- ✅ Gzip compression enabled
- ✅ Cache headers configured
- ✅ Minimal dependencies (0.2 MB)

### Recommended
- Use PostgreSQL for production
- Enable Redis for caching
- Implement rate limiting
- Add monitoring (Sentry, LogRocket)

---

## 🔒 Security Checklist

- ✅ JWT authentication implemented
- ✅ Password hashing (bcrypt)
- ✅ CORS configured
- ✅ Environment variables secured
- ✅ SQL injection protection (SQLAlchemy)
- ✅ No secrets in code
- ⚠️  Add rate limiting (recommended)
- ⚠️  Add HTTPS enforcement (automatic on Vercel)

---

## 📝 Post-Deployment

### 1. Test All Endpoints
- [ ] Health check: `/api/health`
- [ ] API info: `/api/info`
- [ ] Authentication: `/api/auth/register`, `/api/auth/login`
- [ ] Readings: `/api/readings/draw`
- [ ] User profile: `/api/user/profile`

### 2. Configure Domain (Optional)
```bash
vercel domains add yourdomain.com
```

### 3. Set Up Monitoring
- Enable Vercel Analytics
- Add error tracking (Sentry)
- Set up uptime monitoring

### 4. Update Documentation
- Add your Vercel URL to README
- Update API documentation
- Share with users

---

## 🎉 Success!

Your Tarot Místico application is now live on Vercel!

**Next Steps:**
1. ✅ Test all features
2. ✅ Monitor performance
3. ✅ Gather user feedback
4. ✅ Iterate and improve

---

## 📞 Support

- **Validation**: Run `python3 validate.py`
- **Logs**: Run `vercel logs`
- **Documentation**: See `README.md`
- **Vercel Docs**: https://vercel.com/docs

---

**Made with ❤️ and ✨**

*Last updated: December 11, 2025*
