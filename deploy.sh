#!/bin/bash
# Quick Deploy Script for Expense Tracker
# Run this script to prepare your app for deployment

echo "🚀 Preparing Expense Tracker for Cloud Deployment..."
echo ""

# Check if required files exist
echo "📋 Checking deployment files..."
files_to_check=("app.py" "requirements.txt" "Procfile" "templates/base.html")
missing_files=0

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo ""
    echo "❌ Missing files detected. Please ensure all files are present."
    exit 1
fi

echo ""
echo "🔧 Checking app syntax..."

# Test if app has syntax errors
python3 -m py_compile app.py
if [ $? -eq 0 ]; then
    echo "✅ App syntax check passed"
else
    echo "❌ App has syntax errors"
    exit 1
fi

echo ""
echo "📦 Ready for deployment! Choose your platform:"
echo ""
echo "1️⃣  RENDER.COM (Recommended)"
echo "   • Go to: https://render.com"
echo "   • Create 'New Web Service'"
echo "   • Connect GitHub repo or upload files"
echo "   • Build Command: pip install -r requirements.txt"
echo "   • Start Command: gunicorn app:app"
echo ""
echo "2️⃣  RAILWAY.APP (Fastest)"
echo "   • Go to: https://railway.app"
echo "   • Deploy from GitHub repo"
echo "   • Auto-detects settings!"
echo ""
echo "3️⃣  HEROKU (Classic)"
echo "   • Install Heroku CLI"
echo "   • Run: heroku create your-app-name"
echo "   • Run: git push heroku main"
echo ""
echo "🌐 After deployment, your app will be accessible worldwide!"
echo "📱 Share the URL with colleagues for instant access"
echo ""
echo "✨ Files ready for deployment:"
ls -la app.py requirements.txt Procfile DEPLOYMENT.md
echo ""
echo "🎯 Your expense tracker will be live in under 10 minutes!"