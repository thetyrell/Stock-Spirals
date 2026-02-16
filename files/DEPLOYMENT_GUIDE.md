# Deploying Spiral Stock Chart to GitHub

This guide will help you deploy your Spiral Stock Chart to GitHub with:
- **Frontend**: GitHub Pages (free, static hosting)
- **Backend**: Render.com (free tier available) or Railway.app

## Quick Start

### Option 1: GitHub Pages Only (Simplest)
If you just want to see it work, you can deploy only the frontend to GitHub Pages. It will automatically use simulated data.

### Option 2: Full Deployment (Recommended)
Deploy both frontend and backend for the complete experience with the vectorbt-style backend.

---

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon → **New repository**
3. Name it: `spiral-stock-chart`
4. Make it **Public**
5. Initialize with a README (optional)
6. Click **Create repository**

---

## Step 2: Upload Your Files to GitHub

### Using GitHub Web Interface (Easiest)

1. In your new repository, click **Add file** → **Upload files**
2. Drag and drop these files:
   - `backend.py`
   - `SpiralGrok_Updated.html`
   - `README.md`
3. Create additional files (click **Add file** → **Create new file**):

#### Create `requirements.txt`:
```
flask==3.0.0
flask-cors==4.0.0
numpy==1.26.2
pandas==2.1.4
gunicorn==21.2.0
```

#### Create `index.html`:
Just copy the entire contents of `SpiralGrok_Updated.html` into `index.html`
(GitHub Pages looks for `index.html` as the main page)

4. Commit the files

### Using Git Command Line (Alternative)

```bash
# Clone your repository
git clone https://github.com/YOUR-USERNAME/spiral-stock-chart.git
cd spiral-stock-chart

# Copy your files
# (Copy backend.py, SpiralGrok_Updated.html, README.md here)

# Create requirements.txt and index.html as shown above

# Add and commit
git add .
git commit -m "Initial commit: Spiral Stock Chart"
git push origin main
```

---

## Step 3: Deploy Backend to Render.com (Free)

### 3.1 Sign Up for Render

1. Go to [Render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 3.2 Create Web Service

1. Click **New +** → **Web Service**
2. Connect your `spiral-stock-chart` repository
3. Configure the service:
   - **Name**: `spiral-stock-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend:app`
   - **Instance Type**: `Free`
4. Click **Create Web Service**

### 3.3 Get Your Backend URL

After deployment (takes 2-3 minutes), you'll get a URL like:
```
https://spiral-stock-backend.onrender.com
```

**Important**: Free tier on Render spins down after 15 minutes of inactivity. First load will be slow (15-30 seconds).

---

## Step 4: Update Frontend with Backend URL

### 4.1 Edit index.html on GitHub

1. In your repository, click on `index.html`
2. Click the **pencil icon** (Edit this file)
3. Find this line (around line 194):
```javascript
var BACKEND_URL = 'http://localhost:5000';
```

4. Replace it with your Render URL:
```javascript
var BACKEND_URL = 'https://spiral-stock-backend.onrender.com';
```

5. Click **Commit changes**

---

## Step 5: Enable GitHub Pages

1. In your repository, go to **Settings**
2. Scroll down to **Pages** (in the left sidebar)
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 1-2 minutes for deployment

Your site will be available at:
```
https://YOUR-USERNAME.github.io/spiral-stock-chart/
```

---

## Alternative: Deploy Backend to Railway.app

Railway offers 500 hours/month free (also sleeps when inactive).

### Railway Setup

1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your `spiral-stock-chart` repository
5. Railway auto-detects Python and deploys
6. Click on your service → **Settings** → **Generate Domain**
7. Copy the domain (e.g., `spiral-stock-backend.up.railway.app`)
8. Update `BACKEND_URL` in your `index.html` as shown above

---

## Alternative: Heroku (Requires Credit Card)

If you have a Heroku account:

### Create Procfile
```
web: gunicorn backend:app
```

### Deploy
```bash
heroku create spiral-stock-backend
git push heroku main
heroku open
```

Update frontend with: `https://spiral-stock-backend.herokuapp.com`

---

## Verification Steps

### Test Backend Directly

Visit your backend URL + `/api/health`:
```
https://spiral-stock-backend.onrender.com/api/health
```

You should see:
```json
{
  "status": "healthy",
  "version": "1.0",
  "backend": "vectorbt-style"
}
```

### Test Frontend

1. Visit your GitHub Pages URL
2. Check the status indicator (should be green: "Backend connected ✓")
3. Click **Load Stock Data**
4. Stocks should show "(vectorbt)" in the legend

---

## Troubleshooting

### Backend shows "offline"

**Problem**: Frontend can't reach backend

**Solutions**:
1. Check backend URL is correct in `index.html`
2. Make sure backend URL uses `https://` not `http://`
3. Visit backend health endpoint directly to verify it's running
4. On Render free tier, first load takes 15-30 seconds (server is "waking up")

### CORS Errors

**Problem**: Browser blocks requests

**Solution**: Backend already has CORS enabled. If still seeing errors:
1. Make sure you're accessing via GitHub Pages URL (not opening file locally)
2. Check browser console for specific error
3. Verify Flask-CORS is in requirements.txt

### 502 Bad Gateway on Backend

**Problem**: Backend crashed or not started

**Solutions**:
1. Check Render/Railway logs for errors
2. Verify `requirements.txt` is correct
3. Make sure start command is: `gunicorn backend:app`
4. Check if free tier hours are exhausted (Render resets monthly)

### Backend is slow

**Problem**: Free tier servers sleep after inactivity

**Solutions**:
- First load will be slow (15-30 seconds) as server wakes up
- Subsequent loads will be fast
- Consider upgrading to paid tier for always-on service
- Or use simulated data mode (uncheck backend in future feature)

---

## Repository Structure

Your final repository should look like:

```
spiral-stock-chart/
├── backend.py              # Flask API server
├── index.html              # Main frontend page
├── SpiralGrok_Updated.html # Original (keep as backup)
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
└── .gitignore             # Optional (ignore __pycache__, venv)
```

### Optional: Add .gitignore

Create `.gitignore`:
```
__pycache__/
*.pyc
venv/
.env
*.log
```

---

## Cost Breakdown

### Completely Free Setup:
- **GitHub Repository**: Free
- **GitHub Pages**: Free (public repos)
- **Render.com Free Tier**: Free (with 750 hours/month)
- **Railway Free Tier**: Free (500 hours/month + $5 credit)

**Total**: $0/month

### Limitations of Free Tier:
- Backend sleeps after 15 mins inactivity
- First load after sleep: 15-30 seconds
- Render: 750 hours/month (≈31 days if always-on)
- Railway: 500 hours/month

---

## Making Backend Always-On (Optional)

### Option 1: Upgrade to Paid Tier
- Render: $7/month for always-on
- Railway: $5/month for always-on

### Option 2: Keep-Alive Service (Free Hack)
Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your backend every 5 minutes:
1. Sign up (free)
2. Add monitor with your backend URL
3. Set check interval: 5 minutes
4. Backend won't sleep if pinged regularly

**Note**: Some platforms consider this abuse. Check ToS first.

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Upload files + create requirements.txt
3. ✅ Deploy backend to Render/Railway
4. ✅ Update frontend with backend URL
5. ✅ Enable GitHub Pages
6. ✅ Test the deployment
7. 🎉 Share your URL!

---

## Support

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **GitHub Pages**: https://pages.github.com

## Your Live URLs

After setup, you'll have:
- **Frontend**: `https://YOUR-USERNAME.github.io/spiral-stock-chart/`
- **Backend**: `https://spiral-stock-backend.onrender.com` (or Railway)

Share these with anyone! 🚀
