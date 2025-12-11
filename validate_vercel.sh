#!/bin/bash

echo "🔍 Vercel Configuration Validation"
echo "=================================="
echo ""

# Check vercel.json
echo "1. Checking vercel.json..."
if [ -f "vercel.json" ]; then
    echo "   ✅ vercel.json exists"
    
    # Validate JSON syntax
    if python3 -m json.tool vercel.json > /dev/null 2>&1; then
        echo "   ✅ Valid JSON syntax"
    else
        echo "   ❌ Invalid JSON syntax"
        exit 1
    fi
    
    # Check for conflicting properties
    if grep -q '"builds"' vercel.json; then
        echo "   ❌ ERROR: 'builds' property found (conflicts with 'functions')"
        exit 1
    else
        echo "   ✅ No 'builds' property (good)"
    fi
    
    if grep -q '"functions"' vercel.json; then
        echo "   ✅ 'functions' property found"
    else
        echo "   ❌ ERROR: 'functions' property missing"
        exit 1
    fi
    
    if grep -q '"rewrites"' vercel.json; then
        echo "   ✅ 'rewrites' property found"
    else
        echo "   ⚠️  WARNING: 'rewrites' property missing"
    fi
else
    echo "   ❌ vercel.json not found"
    exit 1
fi

echo ""
echo "2. Checking API entry point..."
if [ -f "api/index.py" ]; then
    echo "   ✅ api/index.py exists"
    
    # Check Python syntax
    if python3 -m py_compile api/index.py 2>/dev/null; then
        echo "   ✅ Valid Python syntax"
    else
        echo "   ❌ Invalid Python syntax"
        exit 1
    fi
    
    # Check for Flask app export
    if grep -q "app = Flask" api/index.py; then
        echo "   ✅ Flask app instance found"
    else
        echo "   ❌ Flask app instance not found"
        exit 1
    fi
else
    echo "   ❌ api/index.py not found"
    exit 1
fi

echo ""
echo "3. Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt exists"
    wc -l < requirements.txt | xargs echo "   📦 Dependencies:" 
else
    echo "   ❌ requirements.txt not found"
    exit 1
fi

echo ""
echo "4. Checking static files..."
if [ -f "public/tarot_web.html" ]; then
    echo "   ✅ public/tarot_web.html exists"
else
    echo "   ❌ public/tarot_web.html not found"
    exit 1
fi

if [ -f "public/tarot_web.js" ]; then
    echo "   ✅ public/tarot_web.js exists"
else
    echo "   ❌ public/tarot_web.js not found"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ All validation checks passed!"
echo ""
echo "Ready to deploy with: vercel --prod"
echo "=================================="
