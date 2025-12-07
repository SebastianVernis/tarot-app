# Render Deployment - Tarot App

## Quick Deploy to Render

### Method 1: Blueprint (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "feat: add Render deployment configuration"
   git push origin main
   ```

2. **Deploy via Render Dashboard**
   - Go to https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select branch: `main`
   - Render will read `render.yaml` automatically

3. **Wait for Deploy** (~30 seconds)
   - Static sites deploy instantly
   - No build process needed

### Method 2: Manual Setup

1. **Create Static Site**
   - Go to https://dashboard.render.com
   - Click "New" → "Static Site"
   - Connect repository

2. **Configure Service**
   - **Name**: `tarot-reader`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Build Command**: (leave empty or `echo "No build needed"`)
   - **Publish Directory**: `.` (root)

3. **Configure Routes**
   Add rewrite rule:
   - **Source**: `/`
   - **Destination**: `/tarot_web.html`
   - **Type**: Rewrite

4. **Configure Headers** (Optional)
   Add cache header:
   - **Path**: `/*`
   - **Header**: `Cache-Control`
   - **Value**: `public, max-age=3600`

## Post-Deployment

### Verify Deployment
```bash
# Open in browser
open https://your-app.onrender.com/

# Check HTML loads
curl https://your-app.onrender.com/
```

### Test Functionality
1. Open the deployed URL
2. Select a tirada type (reading type)
3. Optionally enter a question
4. Click "Comenzar Lectura"
5. Verify cards display correctly
6. Check randomness quality indicators

## File Structure Check

Ensure these files are in repository:
```
tarot-app/
├── tarot_web.html      ✓ Main interface
├── tarot_web.js        ✓ JavaScript logic
├── tarot_reader.py     ✓ CLI version (not used in web)
├── requirements.txt    ✓ For local development
├── render.yaml         ✓ Render configuration
└── RENDER_DEPLOY.md    ✓ This file
```

## Important Notes

### No Backend Required
- This is a **pure static site**
- All logic runs in browser
- No server-side processing
- No Python runtime needed for web version

### Python Scripts (Optional)
The Python scripts (`tarot_reader.py`, etc.) are for CLI usage:
- **Not needed** for web deployment
- Can be kept in repo for reference
- Won't affect static site deployment

### Randomness
- Uses browser's `crypto.getRandomValues()`
- High-quality cryptographic randomness
- No external APIs needed

## Troubleshooting

### 404 on Root Path
**Problem**: Homepage doesn't load

**Solution**: Configure rewrite rule
```
Source: /
Destination: /tarot_web.html
Type: Rewrite
```

### JavaScript Not Loading
**Problem**: `tarot_web.js` not found

**Solutions**:
1. Verify `tarot_web.js` is in repository
2. Check file path is relative (not absolute)
3. Check browser console for errors

### Styles Not Working
**Problem**: CSS not loading

**Solutions**:
1. Check if CSS is inline in HTML
2. If external CSS file, verify it's in repo
3. Check relative paths

### Cards Not Displaying
**Problem**: Tarot cards not showing

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify `tarot_web.js` has complete deck data
3. Check `TAROT_DB` object in JavaScript

## Performance

### Load Time
- **Expected**: <1 second
- **Actual**: Usually 200-500ms
- **Optimizations**:
  - Enable Render CDN
  - Compress assets
  - Minify JavaScript (optional)

### Caching
- Static assets cached by CDN
- Browser cache: 1 hour (3600s)
- Can increase for better performance

## Cost

### Free Tier
- **Perfect for this use case**
- Unlimited bandwidth (fair use)
- Global CDN included
- Custom domain supported
- SSL certificate included

### No Paid Plan Needed
Static sites on Render free tier are sufficient for:
- Personal projects
- Public demos
- Production use (reasonable traffic)

## Customization

### Change Appearance
Edit `tarot_web.html`:
- CSS styles are inline
- Modify colors, fonts, layouts
- Add custom imagery

### Add Features
Edit `tarot_web.js`:
- Add new tirada types
- Modify interpretations
- Add statistics tracking
- Implement history

### Add Analytics
Add to `tarot_web.html`:
```html
<!-- Google Analytics example -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

## Custom Domain

1. **Add Domain in Render**
   - Go to your static site settings
   - Click "Custom Domains"
   - Add your domain

2. **Configure DNS**
   - Add CNAME record pointing to Render
   - Wait for DNS propagation (up to 48h)
   - SSL certificate auto-provisioned

## Monitoring

### Uptime Monitoring
- Static sites rarely go down
- No server to crash
- Render handles infrastructure

### Usage Analytics
Options:
1. Google Analytics
2. Plausible Analytics (privacy-focused)
3. Simple Analytics
4. Custom solution

## Development Workflow

### Local Testing
```bash
# Open HTML file directly in browser
open tarot_web.html

# Or use local server
python3 -m http.server 8000
# Then open http://localhost:8000/tarot_web.html
```

### Making Changes
```bash
# Edit files
# ... make changes to tarot_web.html or tarot_web.js ...

# Test locally
open tarot_web.html

# Commit and push
git add .
git commit -m "feat: description"
git push origin main

# Render auto-deploys (takes ~30 seconds)
```

## Advanced Features

### Progressive Web App (PWA)
Convert to PWA for offline use:
1. Add `manifest.json`
2. Add service worker
3. Configure caching strategy

### Mobile Optimization
Already responsive but can improve:
- Add touch gestures
- Optimize for mobile keyboards
- Add haptic feedback

### Multi-language Support
Easy to add:
1. Create language files
2. Add language selector
3. Load translations dynamically

## Troubleshooting Build Issues

### Git Issues
```bash
# Check if files are tracked
git status

# Ensure all files are committed
git add .
git commit -m "fix: ensure all files tracked"
git push origin main
```

### File Permissions
Render needs read access to all files:
```bash
# Check locally
ls -la

# Files should be readable (r-- or rw-)
```

## Support

- Render Static Sites: https://render.com/docs/static-sites
- Project Docs: See `CRUSH.md` and `README.md`
- Workspace Guide: See `DEPLOYMENT.md`

## Quick Reference

### URLs After Deploy
```
Production:  https://tarot-reader.onrender.com
Settings:    https://dashboard.render.com/static/[service-id]
Logs:        Minimal (static site)
```

### No Environment Variables Needed
Static sites don't use environment variables.

### No Secrets Required
All code runs in browser, no API keys needed.

### Deploy Time
~30 seconds from push to live.
