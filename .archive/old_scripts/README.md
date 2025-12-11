# 🛠️ Scripts Directory

This directory contains build, deployment, and utility scripts for the Tarot App.

## 📜 Available Scripts

### `build.sh` - Build Validation Script

**Purpose**: Validates the application is ready for Vercel deployment

**Usage**:
```bash
./scripts/build.sh
```

**What it checks**:
- ✅ Python version compatibility
- ✅ Project structure (api/, vercel.json)
- ✅ Requirements.txt optimization
- ✅ Dependency size estimation
- ✅ Python syntax validation
- ✅ Environment variables
- ✅ Static files presence

**Output**:
- Colored terminal output with validation results
- Estimated deployment size
- Missing environment variables warnings
- Build readiness confirmation

**Exit codes**:
- `0` - All checks passed, ready to deploy
- `1` - Validation failed, fix issues before deploying

**Example output**:
```
🔮 Tarot App - Vercel Build Validation
========================================

✅ Python version: 3.9.24
✅ API entry point found
✅ vercel.json found
✅ Requirements optimized for Vercel
✅ Estimated size (45 MB) is within safe limits
✅ Python syntax OK
✅ Frontend HTML found
✅ Frontend JavaScript found

========================================
📊 Build Validation Summary
========================================
✅ Build validation complete! Ready for deployment.
```

---

### `deploy.sh` - General Deployment Script

**Purpose**: Generic deployment script for various platforms

**Usage**:
```bash
./scripts/deploy.sh
```

**Features**:
- Platform-agnostic deployment logic
- Environment validation
- Pre-deployment checks
- Post-deployment verification

---

### `deploy-vercel.sh` - Vercel-Specific Deployment

**Purpose**: Automated Vercel deployment with validation

**Usage**:
```bash
./scripts/deploy-vercel.sh
```

**What it does**:
1. Runs build validation (`build.sh`)
2. Checks Vercel CLI installation
3. Verifies authentication
4. Deploys to Vercel production
5. Validates deployment success
6. Displays deployment URL

**Prerequisites**:
- Vercel CLI installed (`npm i -g vercel`)
- Logged in to Vercel (`vercel login`)
- Environment variables set in Vercel dashboard

**Example**:
```bash
# First time setup
npm i -g vercel
vercel login

# Deploy
./scripts/deploy-vercel.sh
```

---

## 🚀 Quick Deployment Workflow

### 1. Validate Build
```bash
./scripts/build.sh
```

### 2. Deploy to Vercel
```bash
# Option A: Use deployment script
./scripts/deploy-vercel.sh

# Option B: Manual deployment
vercel --prod
```

### 3. Set Environment Variables (First time only)
```bash
vercel env add SECRET_KEY
vercel env add JWT_SECRET_KEY
vercel env add GEMINI_API_KEY
vercel env add DATABASE_URL  # Optional
```

### 4. Verify Deployment
```bash
curl https://your-app.vercel.app/api/health
```

---

## 🔧 Script Maintenance

### Making Scripts Executable

If scripts lose executable permissions:
```bash
chmod +x scripts/*.sh
```

### Running from Project Root

All scripts are designed to run from the project root:
```bash
# From project root
./scripts/build.sh

# Or from scripts directory
cd scripts
./build.sh
```

Scripts automatically change to the project root directory using:
```bash
cd "$(dirname "$0")/.."
```

---

## 📝 Script Development Guidelines

### Adding New Scripts

1. **Create script in `scripts/` directory**
   ```bash
   touch scripts/my-script.sh
   chmod +x scripts/my-script.sh
   ```

2. **Add shebang and error handling**
   ```bash
   #!/bin/bash
   set -e  # Exit on error
   cd "$(dirname "$0")/.."  # Change to project root
   ```

3. **Use colored output for clarity**
   ```bash
   GREEN='\033[0;32m'
   RED='\033[0;31m'
   NC='\033[0m'
   
   echo -e "${GREEN}✅ Success${NC}"
   echo -e "${RED}❌ Error${NC}"
   ```

4. **Document in this README**

### Best Practices

- ✅ Always use `set -e` to exit on errors
- ✅ Change to project root at script start
- ✅ Use colored output for better UX
- ✅ Validate prerequisites before running
- ✅ Provide clear error messages
- ✅ Return appropriate exit codes
- ✅ Document usage and examples

---

## 🐛 Troubleshooting

### Script Not Executable
```bash
chmod +x scripts/build.sh
```

### Script Not Found
```bash
# Make sure you're in project root
cd /path/to/tarot-app
./scripts/build.sh
```

### Python Not Found
```bash
# Check Python installation
python3 --version

# Install Python 3.9+
# On Ubuntu/Debian: sudo apt install python3
# On macOS: brew install python3
```

### Vercel CLI Not Found
```bash
# Install Vercel CLI
npm i -g vercel

# Verify installation
vercel --version
```

---

## 📚 Related Documentation

- **[Build Guide](../docs/VERCEL_BUILD_GUIDE.md)** - Comprehensive build documentation
- **[Quick Start](../docs/VERCEL_QUICK_START.md)** - 3-step deployment guide
- **[Deployment Ready](../docs/DEPLOYMENT_READY_VERCEL.md)** - Deployment checklist

---

**Need help?** Run `./scripts/build.sh` for diagnostics or check the [main README](../README.md).
