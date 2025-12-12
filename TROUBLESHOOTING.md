# Troubleshooting Guide - Banking Application

## If the App Stops Working - Step-by-Step Instructions

### Step 1: Check Browser Console
1. Open your browser (Chrome/Firefox/Safari)
2. Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows) to open Developer Tools
3. Go to the **Console** tab
4. Look for any **red error messages**
5. **Copy the error message** - this is crucial for diagnosis

### Step 2: Check Terminal/Server Logs
1. Check the **frontend terminal** where `npm run serve` is running
2. Look for compilation errors (usually in red)
3. Check the **backend terminal** where Flask is running
4. Look for Python errors or tracebacks

### Step 3: Verify Dependencies
```bash
# Navigate to frontend folder
cd frontend

# Check if node_modules exists
ls node_modules

# If missing, reinstall dependencies
npm install

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Step 4: Check for Syntax Errors
```bash
# In frontend folder, try building
cd frontend
npm run build

# Look for errors in the output
# If build fails, note the file and line number mentioned
```

### Step 5: Verify Router Configuration
1. Check `frontend/src/router/index.js`
2. Ensure all imports are correct
3. Verify route paths match component names
4. Check for missing commas in routes array

### Step 6: Check Component Imports
1. Verify all imported components exist:
   - `frontend/src/views/Home.vue`
   - `frontend/src/components/Login.vue`
   - `frontend/src/components/Dashboard.vue`
   - etc.

2. Check import paths are correct:
   - Relative paths: `'../views/Home.vue'`
   - Alias paths: `'@/components/Login.vue'`

### Step 7: Verify Bootstrap CSS
The app uses Bootstrap classes. Check if Bootstrap is loaded:
1. In browser DevTools, go to **Network** tab
2. Refresh the page
3. Look for `bootstrap` CSS files loading
4. If missing, check `main.js` or `index.html` for Bootstrap imports

### Step 8: Check Vue Router Setup
1. Verify `main.js` has: `.use(router)`
2. Check `router/index.js` exports router correctly
3. Ensure `App.vue` has `<router-view/>`

### Step 9: Common Issues and Fixes

#### Issue: "Cannot read property 'push' of undefined"
**Fix**: Component needs router access
```javascript
// In component script:
methods: {
  goToLogin() {
    this.$router.push('/login');
  }
}
```

#### Issue: "Component not found"
**Fix**: Check import path and file exists
```javascript
// Correct import:
import Home from '../views/Home.vue'
```

#### Issue: "Bootstrap classes not working"
**Fix**: Ensure Bootstrap CSS is imported in `main.js` or `index.html`

#### Issue: "Route not found"
**Fix**: Check router configuration in `router/index.js`

### Step 10: Restart Everything
```bash
# Stop all running processes (Ctrl+C)

# Frontend
cd frontend
npm run serve

# Backend (in another terminal)
cd backend
python app.py
# or
flask run
```

### Step 11: Clear Browser Cache
1. Hard refresh: `Cmd+Shift+R` (Mac) / `Ctrl+Shift+R` (Windows)
2. Or clear browser cache completely
3. Try incognito/private mode

### Step 12: Check Git Status
```bash
# See what files changed
git status

# Check if any critical files were accidentally deleted
git diff
```

### Step 13: Revert to Last Working State
```bash
# Find last working commit
git log --oneline

# Restore specific files from last working commit
git checkout <commit-hash> -- frontend/src/views/Home.vue
git checkout <commit-hash> -- frontend/src/components/Dashboard.vue
# etc.
```

### Step 14: Verify Environment
1. Check Node.js version: `node -v` (should be 14+)
2. Check npm version: `npm -v`
3. Check Python version: `python --version` (should be 3.7+)

### Step 15: Check File Permissions
```bash
# Ensure files are readable
ls -la frontend/src/views/Home.vue
ls -la frontend/src/components/
```

## Quick Diagnostic Commands

```bash
# Check for syntax errors in Vue files
cd frontend
npm run lint

# Check build
npm run build

# Check for missing dependencies
npm audit

# Verify router
grep -r "router" frontend/src/router/index.js
```

## Most Common Causes

1. **Missing comma in routes array** - Check `router/index.js`
2. **Incorrect import path** - Verify file exists and path is correct
3. **Router not injected** - Check component uses `this.$router` correctly
4. **Bootstrap CSS not loaded** - Check imports in `main.js` or `index.html`
5. **Component syntax error** - Check for unclosed tags, missing brackets
6. **Port conflicts** - Frontend (usually 8080) or Backend (usually 5000) already in use

## Getting Help

When reporting issues, provide:
1. **Browser console errors** (screenshot or copy text)
2. **Terminal output** (frontend and backend)
3. **What you were doing** when it broke
4. **What page/feature** isn't working
5. **Recent changes** you made

## Emergency Recovery

If nothing works:
```bash
# Restore from last known good commit
git log --oneline
git checkout <last-working-commit-hash>

# Or restore specific critical files
git checkout HEAD -- frontend/src/views/Home.vue
git checkout HEAD -- frontend/src/router/index.js
git checkout HEAD -- frontend/src/main.js
```


