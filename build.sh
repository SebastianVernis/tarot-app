#!/bin/bash
# Vercel Build Validation Script
# Ensures the application is ready for deployment

set -e  # Exit on error

echo "🔮 Tarot App - Vercel Build Validation"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo "ℹ️  $1"
}

# 1. Check Python version
print_info "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python version: $PYTHON_VERSION"

# 2. Check if api directory exists
print_info "Checking project structure..."
if [ ! -d "api" ]; then
    print_error "api/ directory not found"
    exit 1
fi

if [ ! -f "api/index.py" ]; then
    print_error "api/index.py not found"
    exit 1
fi
print_success "API entry point found"

# 3. Check vercel.json
print_info "Checking Vercel configuration..."
if [ ! -f "vercel.json" ]; then
    print_error "vercel.json not found"
    exit 1
fi
print_success "vercel.json found"

# 4. Check requirements.txt
print_info "Checking requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found"
    exit 1
fi

# Check for heavy dependencies (excluding comments)
HEAVY_DEPS=$(grep -v "^#" requirements.txt | grep -E "^(numpy|matplotlib|scipy|pyswisseph)" || true)
if [ -n "$HEAVY_DEPS" ]; then
    print_warning "Heavy dependencies detected in requirements.txt"
    print_warning "This may exceed Vercel's 250 MB limit"
    echo ""
    echo "Heavy dependencies found:"
    echo "$HEAVY_DEPS"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Build cancelled"
        exit 1
    fi
else
    print_success "Requirements optimized for Vercel"
fi

# 5. Estimate package size
print_info "Estimating dependency size..."
TOTAL_SIZE=0
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue
    
    # Extract package name (before ==, >=, etc.)
    PACKAGE=$(echo "$line" | sed 's/[>=<].*//' | xargs)
    
    # Estimate sizes (approximate)
    case "$PACKAGE" in
        Flask) SIZE=5 ;;
        Flask-SQLAlchemy) SIZE=2 ;;
        Flask-JWT-Extended) SIZE=1 ;;
        Flask-CORS) SIZE=1 ;;
        Flask-Migrate) SIZE=2 ;;
        SQLAlchemy) SIZE=10 ;;
        Werkzeug) SIZE=5 ;;
        PyJWT) SIZE=1 ;;
        python-dotenv) SIZE=1 ;;
        pytz) SIZE=2 ;;
        google-generativeai) SIZE=15 ;;
        numpy) SIZE=60 ;;
        matplotlib) SIZE=120 ;;
        scipy) SIZE=90 ;;
        pyswisseph) SIZE=25 ;;
        *) SIZE=2 ;;
    esac
    
    TOTAL_SIZE=$((TOTAL_SIZE + SIZE))
done < requirements.txt

echo "Estimated total size: ${TOTAL_SIZE} MB"

if [ $TOTAL_SIZE -gt 200 ]; then
    print_error "Estimated size (${TOTAL_SIZE} MB) exceeds safe limit (200 MB)"
    print_warning "Deployment may fail due to Vercel's 250 MB limit"
    exit 1
elif [ $TOTAL_SIZE -gt 150 ]; then
    print_warning "Estimated size (${TOTAL_SIZE} MB) is high but within limits"
else
    print_success "Estimated size (${TOTAL_SIZE} MB) is within safe limits"
fi

# 6. Check Python syntax
print_info "Checking Python syntax..."
python3 -m py_compile api/index.py 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Python syntax OK"
else
    print_error "Python syntax errors in api/index.py"
    exit 1
fi

# Check other Python files
for file in *.py; do
    if [ -f "$file" ]; then
        python3 -m py_compile "$file" 2>/dev/null || print_warning "Syntax warning in $file"
    fi
done

# 7. Check for required environment variables
print_info "Checking environment variables..."
REQUIRED_VARS=("SECRET_KEY" "JWT_SECRET_KEY")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    print_warning "Missing environment variables: ${MISSING_VARS[*]}"
    print_info "Set these in Vercel dashboard or use 'vercel env add'"
else
    print_success "All required environment variables present"
fi

# 8. Check static files
print_info "Checking static files..."
if [ ! -f "tarot_web.html" ]; then
    print_warning "tarot_web.html not found"
else
    print_success "Frontend HTML found"
fi

if [ ! -f "tarot_web.js" ]; then
    print_warning "tarot_web.js not found"
else
    print_success "Frontend JavaScript found"
fi

# 9. Summary
echo ""
echo "========================================"
echo "📊 Build Validation Summary"
echo "========================================"
print_success "Python version: $PYTHON_VERSION"
print_success "API entry point: api/index.py"
print_success "Configuration: vercel.json"
print_success "Estimated size: ${TOTAL_SIZE} MB"
echo ""

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    print_warning "Remember to set environment variables in Vercel"
fi

echo ""
print_success "Build validation complete! Ready for deployment."
echo ""
echo "Next steps:"
echo "  1. Deploy to Vercel: vercel --prod"
echo "  2. Set environment variables: vercel env add <VAR_NAME>"
echo "  3. Test deployment: curl https://your-app.vercel.app/api/health"
echo ""
