#!/bin/bash
# Quick Vercel Deployment Script

set -e  # Exit on error

echo "🚀 Tarot App - Vercel Deployment Script"
echo "========================================"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found!"
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
    echo "✅ Vercel CLI installed"
fi

# Verify requirements.txt is optimized
echo "🔍 Checking requirements.txt..."
if grep -q "numpy\|matplotlib\|scipy\|pyswisseph" requirements.txt; then
    echo "⚠️  Warning: Heavy dependencies detected in requirements.txt"
    echo "📝 Using optimized requirements..."
    cp requirements-vercel.txt requirements.txt
    echo "✅ Requirements optimized"
else
    echo "✅ Requirements already optimized"
fi

# Verify api directory exists
if [ ! -d "api" ]; then
    echo "❌ Error: api/ directory not found"
    exit 1
fi

if [ ! -f "api/index.py" ]; then
    echo "❌ Error: api/index.py not found"
    exit 1
fi

echo "✅ API entry point found"

# Verify vercel.json exists
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found"
    exit 1
fi

echo "✅ Vercel configuration found"

# Check Python syntax
echo "🔍 Checking Python syntax..."
python3 -m py_compile api/index.py
echo "✅ Python syntax OK"

echo ""
echo "📊 Deployment Summary:"
echo "  - API Entry: api/index.py"
echo "  - Config: vercel.json"
echo "  - Requirements: Optimized (~50-80 MB)"
echo "  - Features: Tarot readings, Auth, Subscriptions"
echo "  - Astrology: Disabled (heavy deps removed)"
echo ""

# Ask for confirmation
read -p "🚀 Ready to deploy to Vercel? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Deploying to Vercel..."
    echo ""
    
    # Deploy to production
    vercel --prod
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "📝 Next steps:"
    echo "  1. Test your deployment: vercel ls"
    echo "  2. View logs: vercel logs"
    echo "  3. Check health: curl https://your-app.vercel.app/api/health"
    echo ""
else
    echo "❌ Deployment cancelled"
    exit 0
fi
