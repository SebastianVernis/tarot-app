#!/bin/bash
# tarot-app deployment script for Render CLI

set -e

PROJECT_NAME="tarot-app"
SERVICE_NAME="tarot-reader"
BRANCH="master"

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Deploying $PROJECT_NAME to Render${NC}\n"

# Check if Render CLI is available
if ! command -v render &> /dev/null; then
    echo -e "${RED}❌ Render CLI not found${NC}"
    echo "Install: npm install -g @render/cli"
    exit 1
fi

# Check authentication
if ! render whoami &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with Render${NC}"
    echo "Run: render login"
    exit 1
fi

echo -e "${GREEN}✓ Authenticated as: $(render whoami 2>&1 | grep -oP 'email: \K[^,]+')${NC}\n"

# Check git status
echo -e "${BLUE}📋 Checking git status...${NC}"
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠ Uncommitted changes detected${NC}"
    git status --short
    echo ""
    read -p "Commit changes? (y/n): " do_commit
    if [ "$do_commit" = "y" ]; then
        read -p "Commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
    fi
else
    echo -e "${GREEN}✓ No uncommitted changes${NC}"
fi

# Push to GitHub
echo -e "\n${BLUE}⬆️ Pushing to GitHub ($BRANCH)...${NC}"
git push origin $BRANCH

# Check if service exists
echo -e "\n${BLUE}🔍 Checking if service exists...${NC}"
if render services list --output json | jq -e ".[] | select(.name==\"$SERVICE_NAME\")" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Service '$SERVICE_NAME' found${NC}"
    
    # Trigger deploy
    echo -e "\n${BLUE}🚀 Triggering deployment...${NC}"
    echo -e "${YELLOW}⏱ Deploy time: ~30 seconds (static site)${NC}"
    render deploys create --service "$SERVICE_NAME"
    
    echo -e "\n${GREEN}✅ Static site deployment triggered!${NC}"
    
else
    echo -e "${YELLOW}⚠ Service '$SERVICE_NAME' not found${NC}\n"
    echo "Create it via dashboard or CLI:"
    echo ""
    echo "  render services create \\"
    echo "    --name $SERVICE_NAME \\"
    echo "    --type static \\"
    echo "    --branch $BRANCH \\"
    echo "    --buildCommand 'echo No build needed' \\"
    echo "    --publishPath '.' \\"
    echo "    --region oregon \\"
    echo "    --plan free"
    echo ""
    
    read -p "Open dashboard to create service? (y/n): " open_dash
    if [ "$open_dash" = "y" ]; then
        xdg-open "https://dashboard.render.com/select-repo" 2>/dev/null || \
        open "https://dashboard.render.com/select-repo" 2>/dev/null || \
        echo "Open: https://dashboard.render.com/select-repo"
    fi
fi

echo -e "\n${GREEN}✅ Deployment process complete!${NC}"
