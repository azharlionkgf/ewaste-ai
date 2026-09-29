# 🌐 Permanent Deployment Guide — E-Waste Intelligence System
## By: Azhar Fareed Mulla (2SA25MC002)

---

## Option 1: Streamlit Cloud (FREE — Recommended) 🏆

### Step 1: Install Git
1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal

### Step 2: Create GitHub Account & Repository
1. Go to https://github.com — Sign up (free)
2. Click **"New Repository"**
3. Name: `ewaste-intelligence-system`
4. Set to **Public**
5. Click **Create Repository**

### Step 3: Push Code to GitHub
Open terminal in project folder and run:
```bash
cd C:\Users\HP\.gemini\antigravity\scratch\e_waste_project
git init
git add -A
git commit -m "E-Waste Intelligence System v4.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ewaste-intelligence-system.git
git push -u origin main
```

### Step 4: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository: `ewaste-intelligence-system`
5. Main file path: `app/streamlit_app.py`
6. Click **"Deploy"**

### Step 5: Your Permanent Link! 🎉
You'll get a URL like:
```
https://YOUR_USERNAME-ewaste-intelligence-system.streamlit.app
```
This link works on **mobile, laptop, tablet — everywhere!**

> [!NOTE]
> If you use Gemini API for image classification, add your API key in
> Streamlit Cloud → Settings → Secrets

---

## Option 2: Local Network Access (No Internet Needed)

Your app is already accessible on your local network:
- **Your PC:** http://localhost:8501
- **Other devices on same WiFi:** http://YOUR_IP:8501

To find your IP, run in terminal:
```bash
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter.

---

## Option 3: Quick Start (Double-Click)

Just double-click: **START_APP.bat**

This will start the app automatically on http://localhost:8501

---

## 🔐 Login Credentials

| Role | How to Login |
|------|-------------|
| **Normal User** | Click "Enter as User" (no password) |
| **Admin** | Password: `admin@ewaste2025` |

Admin has access to: EDA Explorer, Model Performance, Batch Processing, Dataset Manager

---

## 📱 Access from Mobile

1. Make sure mobile and laptop are on **same WiFi**
2. Find your laptop IP (run `ipconfig` in terminal)
3. Open mobile browser and go to: `http://YOUR_LAPTOP_IP:8501`

That's it! Full app on mobile! 📱
