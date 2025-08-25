# 🚀 Deploy to Streamlit Community Cloud

## Step-by-Step Deployment Instructions

### 1. Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "+" → "New repository"
3. Name it: `mock-salesforce-app` 
4. Make it **Public** (required for free Streamlit Cloud)
5. Click "Create repository"

### 2. Upload Files

Upload these files to your GitHub repository:
- `design_mockup.py` (main app)
- `streamlit_requirements.txt` (dependencies)
- `README.md` (documentation)

**Option A: Drag & Drop (Easy)**
- Open your GitHub repository
- Drag and drop the files from your local folder
- Add commit message: "Initial commit - Salesforce Design Mockup"
- Click "Commit changes"

**Option B: GitHub Desktop (Recommended)**
- Download [GitHub Desktop](https://desktop.github.com)
- Clone your repository
- Copy files to the local repository folder
- Commit and push changes

### 3. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `mock-salesforce-app`
5. Set main file path: `design_mockup.py`
6. Click "Deploy!"

### 4. Share Your App

Once deployed, you'll get a public URL like:
`https://[your-app-name].streamlit.app`

Share this URL with your team for instant access to the mockup tool!

## 🎯 What Your Team Gets

- **Live Design Tool** - Drag, drop, rearrange fields
- **Real-time Preview** - See changes instantly  
- **Multiple Layouts** - Create different design variations
- **Export Capabilities** - Download designs as JSON
- **No Installation** - Works in any web browser

## 🔧 Making Updates

To update your app:
1. Edit files in GitHub (or locally and push)
2. Streamlit Cloud auto-deploys changes
3. Share the same URL - no need to redeploy

---

**Need Help?** 
- Streamlit Cloud is free for public repositories
- App will auto-sleep after inactivity but wakes up when accessed
- You can have up to 3 apps on the free tier
