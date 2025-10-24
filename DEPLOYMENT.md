# Deployment Guide - AI Hackday Expense Tracker

## 🚀 Quick Start (30 seconds)

### Prerequisites
- Python 3.9+ installed
- Git installed

### Option 1: Run Locally (Immediate)
```bash
git clone https://github.com/blunn-ds/AI-Hackday-ExpenseTracker.git
cd AI-Hackday-ExpenseTracker
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Visit: `http://localhost:5000`

### Option 2: Run with Ngrok (Public Access)
```bash
# After local setup above:
# Download ngrok from https://ngrok.com/download
# Sign up for free account and get auth token
./ngrok authtoken YOUR_TOKEN_HERE
./ngrok http 5000
```
Visit the ngrok HTTPS URL provided

## 🌐 Production Deployment Options

### Option 1: Render.com (Recommended)
1. Fork this repository to your GitHub
2. Create account at render.com
3. Connect GitHub repository
4. Deploy as Web Service
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`

### Option 2: Railway.app
1. Fork this repository
2. Create account at railway.app
3. Deploy from GitHub
4. Auto-detects Python and uses Procfile

### Option 3: Heroku
1. Install Heroku CLI
2. Fork repository
3. ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 🔧 Environment Configuration

### Required Files (Already Included)
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment configuration
- `app.py` - Production WSGI application

### Environment Variables (Optional)
- `PORT` - Server port (default: 5000)
- `DEBUG` - Debug mode (default: False)
- `DATABASE_URL` - External database (default: SQLite)

## 📊 Data Management

### Sample Data
The application includes 23 realistic sample expenses totaling $1,145.07 across 6 categories (Food, Transport, Entertainment, Shopping, Bills, Healthcare).

### Data Persistence
- **Development**: `expenses.json` file
- **Production**: SQLite database (`expenses.db`)
- **Migrations**: Automatic between JSON/SQLite

### Backup & Export
- CSV export available in web interface
- HTML reports with charts
- JSON backup via API endpoints

## 🎯 Features Overview

### Core CRUD Operations
- **Create**: Add expenses with category/amount/date
- **Read**: View all expenses with filtering
- **Update**: Modify expense details
- **Delete**: Remove expenses with confirmation

### Analytics & Visualization
- Dashboard with spending statistics
- Category breakdown charts
- Date range filtering
- Export capabilities

### Multiple Interfaces
- **Web Application** (`app.py`) - Main responsive interface
- **CLI Application** (`expense_tracker.py`) - Terminal interface
- **Read-Only Viewer** (`expense_viewer.py`) - Public dashboard
- **REST API** - JSON endpoints for integration

## 🔍 Troubleshooting

### Common Issues
1. **Port already in use**: Change port or kill existing process
2. **Virtual environment**: Ensure `.venv` is activated
3. **Dependencies**: Run `pip install -r requirements.txt`
4. **Permissions**: Ensure write permissions for data files

### Debug Mode
```bash
export DEBUG=True
python app.py
```

### Log Files
Check terminal output for error messages and debugging information.

## 🎨 Customization

### Themes
Modify `templates/base.html` CSS variables:
```css
:root {
  --primary-color: #6c5ce7;
  --secondary-color: #a29bfe;
  --accent-color: #fd79a8;
}
```

### Categories
Edit categories in `expense_tracker.py`:
```python
EXPENSE_CATEGORIES = [
    "Food", "Transport", "Entertainment", 
    "Shopping", "Bills", "Healthcare",
    "Your Custom Category"
]
```

## 📱 Mobile Compatibility

The application is fully responsive and works on:
- iOS Safari
- Android Chrome
- Mobile Firefox
- Tablet interfaces

## 🔒 Security Considerations

### Production Deployment
- Uses HTTPS with cloud providers
- Input validation on all forms
- Error handling prevents data exposure
- No sensitive data in repository

### Development
- Local development only uses HTTP
- Sample data is safe for sharing
- No authentication required (hackday scope)

## 📈 Performance

### Optimization Features
- SQLite database for fast queries
- Efficient JSON handling
- Minimal JavaScript for speed
- Bootstrap CDN for caching

### Scaling Considerations
- SQLite handles thousands of expenses
- Can migrate to PostgreSQL for larger datasets
- Stateless design allows horizontal scaling

## 🎊 Hackday Demo Features

### Key Demonstrations
1. **Dashboard** - Spending overview with statistics
2. **Add Expense** - Form with validation and categories
3. **Expense List** - Filtering and search capabilities
4. **Analytics** - Category breakdowns and charts
5. **Export** - CSV and HTML report generation

### Sample Data Highlights
- Realistic expense amounts ($4.50 - $125.00)
- Diverse categories showing real usage
- Recent dates (October 2025) for relevance
- Balanced spending across categories

## 📞 Support

### Live Demo
**URL**: https://uncategorised-unvitally-sage.ngrok-free.dev
**Status**: Active during hackday presentation

### Contact
Available for questions, demonstrations, and technical discussions during the hackday event.

## Environment Variables (Optional)

Set these in your hosting platform:
- `SECRET_KEY` - Flask secret key for sessions
- `FLASK_ENV` - Set to `production` for production mode

## Testing Your Deployment

Once deployed, test these URLs:
- `/` - Main dashboard
- `/expenses` - View expenses
- `/add_expense` - Add new expense
- `/analytics` - Spending analysis
- `/api/expenses` - JSON API
- `/health` - Health check

## Sharing with Colleagues

After deployment, share your public URL:
- **Example**: `https://expense-tracker-ai-hackday.onrender.com`
- No installation required for users
- Works on any device with internet
- Mobile-friendly responsive design

## Features Available in Deployed Version

🎯 **Full Web Application**:
- Beautiful responsive dashboard
- Add/view/delete expenses
- Category filtering and analytics
- Data export (CSV, JSON)
- REST API endpoints
- Error handling and health monitoring

## Security & Production Notes

✅ **Production Ready**:
- Error handling for all routes
- Input validation and sanitization  
- Health check endpoint for monitoring
- Environment-based configuration
- Proper HTTP status codes

## Next Steps After Deployment

1. **Test all features** on the live site
2. **Share URL** with colleagues
3. **Monitor usage** via hosting platform dashboard
4. **Scale up** if needed (most platforms auto-scale)

## Estimated Deployment Time: 5-10 minutes ⏱️

Choose **Render.com** for the easiest experience - just upload your files and you're live!

---
*Created for AI Hackday 2025 | Expense Tracker Web Application*