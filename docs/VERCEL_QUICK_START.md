# 🚀 Vercel Quick Start - 3 Steps to Deploy

## Prerequisites
- ✅ Build validation passed (run `./build.sh` to verify)
- ✅ Vercel CLI installed (run `npm install -g vercel`)
- ✅ Vercel account (sign up at https://vercel.com)

## Step 1: Login to Vercel
```bash
vercel login
```
Follow the prompts to authenticate.

## Step 2: Deploy to Production
```bash
vercel --prod
```

Follow the prompts:
- **Set up and deploy?** → Yes
- **Which scope?** → Select your account
- **Link to existing project?** → No (first time)
- **Project name?** → tarot-app (or your choice)
- **Directory?** → ./ (press Enter)
- **Override settings?** → No (press Enter)

Wait 2-3 minutes for deployment...

## Step 3: Set Environment Variables
```bash
# Generate secure keys
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Set in Vercel
vercel env add SECRET_KEY
# Paste: $SECRET_KEY

vercel env add JWT_SECRET_KEY
# Paste: $JWT_SECRET_KEY

# Optional: Add database
vercel env add DATABASE_URL
# Enter: postgresql://user:password@host:5432/database
# Or leave empty for in-memory SQLite

# Optional: Add Gemini AI
vercel env add GEMINI_API_KEY
# Enter your Gemini API key
```

## Step 4: Redeploy with Environment Variables
```bash
vercel --prod
```

## ✅ Done! Test Your Deployment

### Health Check
```bash
curl https://your-app.vercel.app/api/health
```

### Open in Browser
```
https://your-app.vercel.app/
```

## 📊 Your URLs
- **Frontend:** https://your-app.vercel.app
- **API:** https://your-app.vercel.app/api
- **Health:** https://your-app.vercel.app/api/health
- **Info:** https://your-app.vercel.app/api/info

## 🔧 Common Commands

### View Logs
```bash
vercel logs --follow
```

### List Deployments
```bash
vercel ls
```

### Remove Deployment
```bash
vercel rm [deployment-url]
```

### Pull Environment Variables
```bash
vercel env pull
```

### Link to Project
```bash
vercel link
```

## 🆘 Troubleshooting

### Build Failed?
```bash
# Run validation
./build.sh

# Check logs
vercel logs
```

### Environment Variables Not Working?
```bash
# Pull variables locally
vercel env pull

# Check .env file
cat .env

# Redeploy
vercel --prod
```

### CORS Errors?
Add your domain to CORS_ORIGINS:
```bash
vercel env add CORS_ORIGINS
# Enter: https://your-domain.com
```

## 📚 More Help
- **Detailed Guide:** `VERCEL_BUILD_GUIDE.md`
- **Deployment Status:** `DEPLOYMENT_READY_VERCEL.md`
- **Build Validation:** `./build.sh`
- **Vercel Docs:** https://vercel.com/docs

---

**That's it! Your app is live! 🎉**
