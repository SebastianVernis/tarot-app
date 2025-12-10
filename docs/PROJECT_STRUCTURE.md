# 📁 Project Structure

## Overview

The Tarot App project has been organized with a clean, modular structure optimized for Vercel deployment.

## Directory Structure

```
/vercel/sandbox/
├── api/                          # Vercel serverless functions
│   └── index.py                  # Main API entry point for Vercel
│
├── src/                          # Python source modules
│   ├── __init__.py
│   ├── auth.py                   # JWT authentication system
│   ├── models.py                 # SQLAlchemy database models
│   ├── middleware.py             # Freemium middleware & limits
│   ├── gemini_service.py         # Google Gemini AI integration
│   ├── tarot_reader.py           # Tarot card reading logic
│   ├── tarot_reader_enhanced.py  # Enhanced tarot features
│   ├── astrology_calculator.py   # Astrology calculations
│   └── astrology_calculator_lite.py  # Lightweight astrology
│
├── routes/                       # Flask route blueprints
│   ├── auth_routes.py            # Authentication endpoints
│   ├── user_routes.py            # User profile & settings
│   ├── reading_routes.py         # Tarot reading endpoints
│   ├── subscription_routes.py    # Subscription management
│   └── astrology_routes.py       # Astrology endpoints
│
├── docs/                         # Documentation
│   ├── PROJECT_STRUCTURE.md      # This file
│   ├── VERCEL_BUILD_GUIDE.md     # Vercel deployment guide
│   ├── VERCEL_QUICK_START.md     # Quick start guide
│   ├── DEPLOYMENT_READY_VERCEL.md # Deployment checklist
│   └── ... (other documentation)
│
├── scripts/                      # Build and deployment scripts
│   ├── build.sh                  # Build validation script
│   ├── deploy-vercel.sh          # Vercel deployment script
│   ├── deploy.sh                 # Render deployment script
│   └── README.md                 # Scripts documentation
│
├── public/                       # Static frontend files
│   ├── tarot_web.html            # Main HTML page
│   ├── tarot_web.js              # Frontend JavaScript
│   └── ... (other static assets)
│
├── utils/                        # Utility scripts
│   └── init_db.py                # Database initialization
│
├── tests/                        # Test files
│   └── test_astrology.py         # Astrology tests
│
├── instance/                     # Instance-specific files (SQLite DB)
│
├── __pycache__/                  # Python cache (ignored)
│
├── .env.example                  # Environment variables template
├── .vercelignore                 # Vercel ignore rules
├── app.py                        # Main Flask application
├── config.py                     # Application configuration
├── Dockerfile                    # Docker configuration
├── README.md                     # Main project README
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render deployment config
└── vercel.json                   # Vercel configuration
```

## Key Files

### Root Directory (Essentials Only)

- **app.py** - Main Flask application factory
- **config.py** - Configuration management (dev/prod/Vercel)
- **requirements.txt** - Python dependencies (~45 MB)
- **vercel.json** - Vercel serverless configuration
- **README.md** - Project documentation
- **.env.example** - Environment variables template
- **Dockerfile** - Docker container configuration
- **render.yaml** - Render platform configuration

### Source Code (`src/`)

All Python modules are organized in the `src/` directory:

- **auth.py** - JWT authentication, token management, login decorators
- **models.py** - Database models (User, Reading, Subscription, BirthChart, etc.)
- **middleware.py** - Freemium limits, reading restrictions
- **gemini_service.py** - Google Gemini AI for interpretations
- **tarot_reader.py** - Core tarot reading logic
- **tarot_reader_enhanced.py** - Advanced tarot features
- **astrology_calculator.py** - Full astrology calculations (heavy)
- **astrology_calculator_lite.py** - Lightweight astrology (Vercel-friendly)

### API Entry Point (`api/`)

- **api/index.py** - Vercel serverless function handler
  - Exports Flask app for Vercel
  - Optimized for 250 MB limit
  - Graceful dependency handling
  - Request/response logging

### Routes (`routes/`)

Flask blueprints for API endpoints:

- **auth_routes.py** - `/api/auth/*` - Login, register, refresh tokens
- **user_routes.py** - `/api/user/*` - Profile, settings, theme
- **reading_routes.py** - `/api/readings/*` - Create/list readings
- **subscription_routes.py** - `/api/subscription/*` - Plans, upgrades
- **astrology_routes.py** - `/api/astrology/*` - Birth charts, aspects

### Documentation (`docs/`)

Comprehensive documentation:

- **PROJECT_STRUCTURE.md** - This file
- **VERCEL_BUILD_GUIDE.md** - Complete Vercel deployment guide
- **VERCEL_QUICK_START.md** - Quick 3-step deployment
- **DEPLOYMENT_READY_VERCEL.md** - Pre-deployment checklist
- **VERCEL_DEPLOYMENT_COMPLETE.md** - Post-deployment guide
- Plus historical docs and implementation guides

### Scripts (`scripts/`)

Build and deployment automation:

- **build.sh** - Pre-deployment validation
  - Checks Python syntax
  - Validates configuration
  - Estimates package size
  - Verifies environment variables
- **deploy-vercel.sh** - Automated Vercel deployment
- **deploy.sh** - Render platform deployment

### Frontend (`public/`)

Static files served by Vercel CDN:

- **tarot_web.html** - Main SPA HTML
- **tarot_web.js** - Frontend JavaScript
- **assets/** - Images, icons, card images

## Import Structure

All imports now use the `src.` prefix:

```python
# ✅ Correct imports
from src.models import User, Reading, db
from src.auth import login_required, create_tokens
from src.middleware import FreemiumMiddleware
from src.gemini_service import GeminiAstrologyService
from src.tarot_reader import LectorTarot
from src.astrology_calculator import AstrologyCalculator

# ❌ Old imports (no longer work)
from models import User  # Wrong!
from auth import login_required  # Wrong!
```

## Configuration Files

### Vercel Configuration (`vercel.json`)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "250mb",
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "public/$1"
    }
  ]
}
```

### Environment Variables

Required environment variables (set in Vercel dashboard):

```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://... (optional, defaults to SQLite)
GEMINI_API_KEY=your-gemini-key (optional)
```

## Development Workflow

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Initialize database
python utils/init_db.py
```

### Testing

```bash
# Validate build
./scripts/build.sh

# Test syntax
python3 -m py_compile app.py api/index.py

# Run tests
python tests/test_astrology.py
```

### Deployment

```bash
# Deploy to Vercel
vercel --prod

# Or use automated script
./scripts/deploy-vercel.sh
```

## Features by Directory

### Core Features (`src/`)
- ✅ JWT Authentication
- ✅ User Management
- ✅ Freemium System
- ✅ Database Models
- ✅ Tarot Reading Logic
- ✅ AI Interpretations

### API Features (`routes/`)
- ✅ RESTful API
- ✅ Authentication Endpoints
- ✅ Reading Management
- ✅ Subscription Management
- ✅ User Profiles
- ✅ Astrology Calculations

### Frontend Features (`public/`)
- ✅ Responsive SPA
- ✅ Dark/Light Theme
- ✅ Interactive Card Selection
- ✅ Reading History
- ✅ User Dashboard

## Size Optimization

### Vercel Deployment (~45 MB)
- ✅ Core Flask dependencies
- ✅ SQLAlchemy (lightweight)
- ✅ JWT authentication
- ✅ Google Gemini AI
- ❌ Heavy astrology libs (optional)

### Full Deployment (~150 MB)
- ✅ All core features
- ✅ Full astrology calculations
- ✅ pyswisseph library
- ✅ numpy, matplotlib

## Next Steps

1. **Deploy to Vercel**: `vercel --prod`
2. **Set Environment Variables**: Use Vercel dashboard
3. **Test Deployment**: `curl https://your-app.vercel.app/api/health`
4. **Monitor Logs**: `vercel logs`

## Documentation

- 📖 **Quick Start**: `docs/VERCEL_QUICK_START.md`
- 📖 **Full Guide**: `docs/VERCEL_BUILD_GUIDE.md`
- 📖 **Scripts**: `scripts/README.md`
- 📖 **Main README**: `README.md`

---

**Project organized and ready for deployment! 🚀**
