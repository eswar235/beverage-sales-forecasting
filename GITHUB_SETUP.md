# 🚀 GitHub Setup Guide

## Step-by-Step Instructions to Push to GitHub

---

### **Step 1: Initialize Git Repository**

Open PowerShell in your project folder and run:

```bash
git init
```

---

### **Step 2: Add All Files**

```bash
git add .
```

---

### **Step 3: Create First Commit**

```bash
git commit -m "Initial commit: Beverage Sales Forecasting System"
```

---

### **Step 4: Create GitHub Repository**

1. Go to [GitHub.com](https://github.com)
2. Click the **"+"** icon (top right)
3. Click **"New repository"**
4. Fill in:
   - **Repository name:** `beverage-sales-forecasting`
   - **Description:** `End-to-end ML forecasting system with ARIMA, Prophet, and XGBoost`
   - **Public** or **Private** (your choice)
   - **DON'T** check "Initialize with README" (we already have one)
5. Click **"Create repository"**

---

### **Step 5: Connect to GitHub**

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/beverage-sales-forecasting.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

### **Step 6: Push to GitHub**

```bash
git push -u origin main
```

**If asked for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)

---

### **How to Create Personal Access Token:**

1. Go to GitHub → Settings → Developer settings
2. Click "Personal access tokens" → "Tokens (classic)"
3. Click "Generate new token (classic)"
4. Give it a name: "Forecasting Project"
5. Select scopes: Check **"repo"**
6. Click "Generate token"
7. **COPY THE TOKEN** (you won't see it again!)
8. Use this token as your password when pushing

---

### **Alternative: Use GitHub Desktop (Easier!)**

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in
3. Click "Add" → "Add existing repository"
4. Select your project folder
5. Click "Publish repository"
6. Done! ✅

---

## 📝 Quick Commands Summary

```bash
# Initialize
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Beverage Sales Forecasting System"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/beverage-sales-forecasting.git

# Push
git branch -M main
git push -u origin main
```

---

## 🎯 What Gets Pushed to GitHub:

✅ **Included:**
- All source code (`src/`)
- API code (`api/`)
- Data files (`data/`)
- Documentation (README, guides)
- Requirements file
- Demo scripts
- Test HTML page

❌ **Excluded (via .gitignore):**
- Virtual environment (`.venv/`)
- Python cache (`__pycache__/`)
- Trained models (`.pkl` files - too large)
- IDE settings

---

## 🔄 Future Updates

After making changes, push updates with:

```bash
git add .
git commit -m "Description of changes"
git push
```

---

## ✅ Verify Upload

After pushing, go to:
```
https://github.com/YOUR_USERNAME/beverage-sales-forecasting
```

You should see all your files! 🎉

---

## 📱 Share Your Project

Your project URL will be:
```
https://github.com/YOUR_USERNAME/beverage-sales-forecasting
```

Share this link in your video description! 🚀
