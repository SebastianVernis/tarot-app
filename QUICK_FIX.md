# 🚀 QUICK FIX - Vercel Deployment

## Problem
```
Error: A Serverless Function has exceeded the unzipped maximum size of 250 MB
```

## Solution (30 seconds)

### Option A: Deploy to Vercel (No Astrology)
```bash
vercel --prod
```
✅ **Done!** Your app is live in ~2 minutes.

### Option B: Deploy to Render (Full Features)
```bash
# 1. Restore full requirements
cp requirements-original.txt requirements.txt

# 2. Push to GitHub
git add .
git commit -m "deploy to Render"
git push origin master

# 3. Deploy via Render Dashboard
# https://dashboard.render.com → New → Web Service
```
✅ **Done!** All features including astrology.

---

## What Changed?

### Files Created
- ✅ `vercel.json` - Vercel config
- ✅ `api/index.py` - Serverless entry point
- ✅ `requirements.txt` - Optimized (50-80 MB)
- ✅ `.vercelignore` - Exclude unnecessary files

### Dependencies Removed (for Vercel)
- ❌ numpy (~50-80 MB)
- ❌ matplotlib (~100-150 MB)
- ❌ scipy (~80-100 MB)
- ❌ pyswisseph (~20-30 MB)

### Features Available

**Vercel (Optimized):**
- ✅ Tarot readings
- ✅ Authentication
- ✅ Subscriptions
- ❌ Astrology (disabled)

**Render (Full):**
- ✅ Everything above
- ✅ Astrology birth charts
- ✅ Planetary calculations

---

## Quick Commands

### Deploy to Vercel
```bash
vercel --prod
```

### Deploy to Render
```bash
cp requirements-original.txt requirements.txt
git add . && git commit -m "deploy" && git push
# Then: Render Dashboard → Deploy
```

### Test Locally
```bash
python app.py
curl http://localhost:5000/api/health
```

### Check Deployment
```bash
# Vercel
vercel ls
vercel logs

# Render
# Dashboard: https://dashboard.render.com
```

---

## Recommendation

**For Quick Testing:** Use Vercel (2 min deploy)  
**For Production:** Use Render (all features)

---

## Need Help?

Read full guide: `VERCEL_DEPLOYMENT_FIX.md`

---

**TL;DR:** Run `vercel --prod` to deploy now! 🚀
