# 🚀 Vercel Build & Deployment Guide - Complete

## Overview

This guide provides complete instructions for building and deploying the Tarot application to Vercel with optimized serverless configuration.

## ✅ What's Been Configured

### 1. **vercel.json** - Optimized Configuration
- ✅ Serverless function routing for API endpoints
- ✅ Static file serving with proper caching headers
- ✅ SPA routing support
- ✅ Python 3.11 runtime
- ✅ Increased memory (1024 MB) and timeout (30s)
- ✅ Proper rewrites and routes configuration

### 2. **api/index.py** - Enhanced Entry Point
- ✅ Proper WSGI app export for Vercel
- ✅ Logging and error handling
- ✅ Database initialization on first request
- ✅ Graceful handling of missing dependencies
- ✅ Request/response logging middleware
- ✅ CORS configuration with proper headers

### 3. **config.py** - Vercel-Optimized Settings
- ✅ Automatic Vercel environment detection
- ✅ Database URL handling (PostgreSQL/SQLite)
- ✅ Connection pooling optimized for serverless
- ✅ CORS origins including Vercel domains
- ✅ Environment variable configuration
- ✅ Production-ready settings

### 4. **build.sh** - Pre-Deployment Validation
- ✅ Python version check
- ✅ Project structure validation
- ✅ Dependency size estimation
- ✅ Syntax checking
- ✅ Environment variable verification
- ✅ Static file checks

### 5. **requirements.txt** - Optimized Dependencies
- ✅ Lightweight packages (~50-80 MB total)
- ✅ No heavy dependencies (numpy, matplotlib, scipy removed)
- ✅ Core functionality maintained
- ✅ Within Vercel's 250 MB limit

## 📋 Pre-Deployment Checklist

### 1. Verify Requirements
```bash
# Run the build validation script
./build.sh
```

This will check:
- ✅ Python version
- ✅ Project structure
- ✅ Dependency sizes
- ✅ Python syntax
- ✅ Environment variables
- ✅ Static files

### 2. Install Vercel CLI
```bash
npm install -g vercel
```

### 3. Login to Vercel
```bash
vercel login
```

## 🚀 Deployment Steps

### Option 1: Quick Deploy (Recommended)

```bash
# Deploy to production
vercel --prod
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Select your account
- **Link to existing project?** No (first time) / Yes (subsequent)
- **Project name?** tarot-app (or your choice)
- **Directory?** ./ (current directory)
- **Override settings?** No

### Option 2: Preview Deploy (Testing)

```bash
# Deploy to preview environment
vercel
```

This creates a preview URL for testing before production.

### Option 3: Using Deploy Script

```bash
# Use the provided deployment script
./deploy-vercel.sh
```

## 🔧 Environment Variables

### Required Variables

Set these in Vercel dashboard or via CLI:

```bash
# Secret keys (REQUIRED)
vercel env add SECRET_KEY
# Enter: your-secret-key-here

vercel env add JWT_SECRET_KEY
# Enter: your-jwt-secret-key-here

# Database (RECOMMENDED for production)
vercel env add DATABASE_URL
# Enter: postgresql://user:password@host:5432/database
# Or leave empty to use in-memory SQLite (data won't persist)

# Gemini AI (OPTIONAL - for AI interpretations)
vercel env add GEMINI_API_KEY
# Enter: your-gemini-api-key-here

# CORS Origins (OPTIONAL - auto-configured)
vercel env add CORS_ORIGINS
# Enter: https://your-domain.com,https://another-domain.com
```

### Set Environment Variables via Dashboard

1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add each variable:
   - **Name**: Variable name (e.g., SECRET_KEY)
   - **Value**: Variable value
   - **Environment**: Production, Preview, Development (select all)
5. Click **Save**

## 🗄️ Database Configuration

### Option 1: PostgreSQL (Recommended for Production)

Use a managed PostgreSQL service:

**Vercel Postgres:**
```bash
# Install Vercel Postgres
vercel postgres create

# Link to your project
vercel link

# Get connection string
vercel env pull
```

**External Services:**
- [Neon](https://neon.tech) - Free tier available
- [Supabase](https://supabase.com) - Free tier available
- [Railway](https://railway.app) - Free tier available

Set the DATABASE_URL:
```bash
vercel env add DATABASE_URL
# Enter: postgresql://user:password@host:5432/database
```

### Option 2: SQLite In-Memory (Development Only)

If no DATABASE_URL is set, the app uses in-memory SQLite:
- ⚠️ Data is lost on each deployment
- ⚠️ Data is lost when function goes cold
- ✅ Good for testing
- ❌ Not suitable for production

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
# Replace with your actual Vercel URL
curl https://your-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Tarot API",
  "version": "1.0.0",
  "platform": "Vercel",
  "features": {
    "auth": true,
    "readings": true,
    "subscriptions": true,
    "astrology": false
  }
}
```

### 2. API Info
```bash
curl https://your-app.vercel.app/api/info
```

### 3. Frontend
Open in browser:
```
https://your-app.vercel.app/
```

### 4. Test Authentication
```bash
# Register a user
curl -X POST https://your-app.vercel.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
  }'

# Login
curl -X POST https://your-app.vercel.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

## 📊 Monitoring & Logs

### View Logs
```bash
# Real-time logs
vercel logs --follow

# Recent logs
vercel logs

# Logs for specific deployment
vercel logs [deployment-url]
```

### View in Dashboard
1. Go to https://vercel.com/dashboard
2. Select your project
3. Click on **Deployments**
4. Click on a deployment
5. View **Logs** tab

## 🔍 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Verify requirements.txt has all dependencies
cat requirements.txt

# Check if package is listed
grep -i "package-name" requirements.txt

# Add missing package
echo "package-name==version" >> requirements.txt

# Redeploy
vercel --prod
```

### Issue: "Database locked" errors

**Solution:**
SQLite doesn't work well on serverless. Use PostgreSQL:
```bash
vercel env add DATABASE_URL
# Enter PostgreSQL connection string
```

### Issue: "Function size exceeded 250 MB"

**Solution:**
```bash
# Check requirements.txt for heavy packages
grep -E "numpy|matplotlib|scipy|pyswisseph" requirements.txt

# Remove heavy packages if found
# Use the optimized requirements.txt

# Verify size
./build.sh
```

### Issue: CORS errors

**Solution:**
```bash
# Add your domain to CORS_ORIGINS
vercel env add CORS_ORIGINS
# Enter: https://your-domain.com,https://another-domain.com

# Or update config.py to include your domain
```

### Issue: Cold start slow

**Solution:**
This is normal for serverless functions. First request after idle takes 2-5 seconds.

To minimize:
- Use Vercel Pro plan (keeps functions warm)
- Optimize imports (lazy loading)
- Use connection pooling (already configured)

### Issue: Environment variables not working

**Solution:**
```bash
# Pull environment variables locally
vercel env pull

# Check .env file
cat .env

# Verify in Vercel dashboard
# Settings → Environment Variables

# Redeploy after adding variables
vercel --prod
```

## 🎯 Performance Optimization

### 1. Enable Caching
Already configured in vercel.json:
- API responses: No cache
- Static files: 1 year cache

### 2. Use CDN
Vercel automatically uses global CDN for static files.

### 3. Optimize Database Queries
- Use connection pooling (already configured)
- Add database indexes
- Use pagination for large datasets

### 4. Minimize Cold Starts
- Keep functions warm with periodic pings
- Optimize imports
- Use lazy loading

## 📈 Scaling

### Free Tier Limits
- 100 GB bandwidth/month
- 100 hours serverless function execution/month
- Unlimited deployments

### Pro Tier Benefits
- 1 TB bandwidth/month
- 1000 hours serverless function execution/month
- Faster builds
- Functions stay warm longer
- Priority support

## 🔄 Continuous Deployment

### Connect to Git

1. Push your code to GitHub/GitLab/Bitbucket
2. In Vercel dashboard, click **Import Project**
3. Select your repository
4. Vercel will auto-deploy on every push to main branch

### Configure Auto-Deploy

```bash
# Link to Git repository
vercel link

# Set production branch
vercel git connect
```

Now every push to main branch will auto-deploy to production!

## 📝 Post-Deployment Checklist

- [ ] Health check endpoint works
- [ ] API info endpoint works
- [ ] Frontend loads correctly
- [ ] User registration works
- [ ] User login works
- [ ] Tarot readings work
- [ ] Database persists data (if using PostgreSQL)
- [ ] Environment variables are set
- [ ] CORS is configured correctly
- [ ] Logs are accessible
- [ ] Custom domain configured (optional)

## 🌐 Custom Domain

### Add Custom Domain

1. Go to Vercel dashboard
2. Select your project
3. Go to **Settings** → **Domains**
4. Click **Add**
5. Enter your domain
6. Follow DNS configuration instructions

### Configure DNS

Add these records to your DNS provider:

**For apex domain (example.com):**
```
Type: A
Name: @
Value: 76.76.21.21
```

**For subdomain (www.example.com):**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

## 🎉 Success!

Your Tarot application is now deployed to Vercel!

**Your URLs:**
- Production: https://your-app.vercel.app
- API: https://your-app.vercel.app/api
- Health: https://your-app.vercel.app/api/health

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)

## 🆘 Need Help?

- Check logs: `vercel logs`
- Run validation: `./build.sh`
- Check Vercel status: https://vercel-status.com
- Vercel support: https://vercel.com/support

---

**Built with ❤️ for Vercel serverless deployment**
