# Expense Tracker - AI Hackday 2025

**Live Demo**: [Deploy to get your URL]

A comprehensive expense tracking web application built for AI Hackday 2025. Features a beautiful web interface, analytics, and data export capabilities.

## 🚀 Quick Deploy (5 minutes)

### Deploy to Render (Recommended)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Fork this repository
2. Sign up at [Render.com](https://render.com) 
3. Create "New Web Service" from your GitHub repo
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Deploy! ✅

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. Click the Railway button above
2. Sign in with GitHub
3. Auto-deploys! ✅

## 🎯 Features

- **📊 Dashboard** - Beautiful expense overview with statistics
- **➕ Add Expenses** - Clean web forms with validation
- **📋 Expense Management** - View, filter, and delete expenses
- **📈 Analytics** - Visual spending analysis and charts
- **💾 Data Export** - CSV, JSON, and HTML reports
- **🔌 REST API** - JSON endpoints for integration
- **📱 Mobile Friendly** - Responsive design for all devices

## 💡 Tech Stack

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: JSON file storage (easily upgradeable to PostgreSQL)
- **Deployment**: Gunicorn WSGI server
- **Hosting**: Render, Railway, or Heroku compatible

## 🏗 Local Development

```bash
# Clone the repository
git clone [your-repo-url]
cd AI-Hackday-ExpenseTracker

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Open `http://localhost:5000`

## 📊 Sample Data

The application includes 23 sample expenses ($1,049.57 total) across 6 categories:
- Food, Transport, Entertainment, Shopping, Bills, Healthcare

## 🌐 Public Access

Once deployed, your expense tracker will be accessible worldwide via your unique URL. Share it with colleagues, team members, or use it for personal expense tracking from any device.

## 📝 API Endpoints

- `GET /api/expenses` - All expenses as JSON
- `GET /api/stats` - Summary statistics
- `GET /health` - Application health check

## 🏆 AI Hackday 2025

**Challenge**: Create an expense tracker with CRUD operations and visualizations  
**Result**: Full-featured web application with deployment-ready architecture  
**Bonus Features**: Web interface, analytics, export capabilities, REST API

---

**Ready to deploy?** Choose a platform above and have your expense tracker live in under 10 minutes! 🚀