# 🚀 Tarot App - Quick Reference

## 📁 Project Structure

```
/vercel/sandbox/
├── src/              # Python modules (NEW!)
├── routes/           # API blueprints
├── api/              # Vercel serverless
├── docs/             # Documentation
├── scripts/          # Build scripts
├── public/           # Frontend files
├── app.py            # Main Flask app
├── config.py         # Configuration
└── vercel.json       # Vercel config
```

## 🔧 Quick Commands

### Development
```bash
python app.py                    # Run dev server
python utils/init_db.py          # Initialize DB
```

### Testing
```bash
./scripts/build.sh               # Validate build
python3 -m py_compile app.py     # Check syntax
```

### Deployment
```bash
vercel --prod                    # Deploy to Vercel
./scripts/deploy-vercel.sh       # Automated deploy
vercel logs                      # View logs
```

## 📚 Documentation

- **Structure**: `docs/PROJECT_STRUCTURE.md`
- **Organization**: `docs/ORGANIZATION_COMPLETE.md`
- **Vercel Guide**: `docs/VERCEL_BUILD_GUIDE.md`
- **Quick Start**: `docs/VERCEL_QUICK_START.md`

## 🔑 Environment Variables

```bash
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://...  # Optional
GEMINI_API_KEY=your-key        # Optional
```

## 📦 Import Structure

```python
# ✅ Correct (NEW)
from src.models import User, db
from src.auth import login_required
from src.middleware import FreemiumMiddleware

# ❌ Old (Don't use)
from models import User
from auth import login_required
```

## 🎯 Key Features

- ✅ JWT Authentication
- ✅ Tarot Readings (all spreads)
- ✅ Freemium System
- ✅ AI Interpretations (Gemini)
- ✅ User Subscriptions
- ✅ Reading History
- ✅ Theme Persistence

## 🚀 Deployment Checklist

- [ ] Run `./scripts/build.sh`
- [ ] Set environment variables in Vercel
- [ ] Deploy with `vercel --prod`
- [ ] Test: `curl https://your-app.vercel.app/api/health`
- [ ] Open in browser

## 📊 Project Stats

- **Root Files**: 9 essential files
- **Python Modules**: 8 in `src/`
- **API Routes**: 5 blueprints
- **Documentation**: 29+ files
- **Build Scripts**: 4 scripts
- **Package Size**: ~45 MB (Vercel optimized)

---

**Ready to deploy! 🎉**
