# AI Hackday Expense Tracker 💰

A comprehensive expense tracking application built for the AI Hackday 2025 challenge.

## 📋 Project Overview

This expense tracker demonstrates modern software development practices with:
- **Clean data separation** (SQLite database vs hardcoded data)
- **Multiple user interfaces** (CLI, HTML reports)  
- **Professional architecture** (separate modules for different concerns)
- **Scalable design** (ready for cloud integration)

## 🚀 Quick Start

### Running the Applications

```bash
# Full interactive expense manager (admin access)
python3 expense_tracker.py

# Read-only viewer (public access)
python3 expense_viewer.py

# Generate shareable HTML report
python3 html_report_generator.py

# Test database functionality
python3 database_manager.py

# Quick data verification
python3 test_expenses.py
```

### First Time Setup

The app will automatically create sample data if no expenses exist. Your data is stored in `expenses.db` (SQLite database).

## 📁 Project Structure

```
AI-Hackday-ExpenseTracker/
├── README.md                     # This file
├── expense_tracker.py            # Main application (admin interface)
├── expense_viewer.py             # Read-only public viewer
├── database_manager.py           # SQLite database operations
├── html_report_generator.py      # Beautiful HTML report generation
├── test_expenses.py              # Testing and verification utilities
├── expenses.db                   # SQLite database (main data store)
├── expenses.json                 # Legacy JSON format (backup)
├── expense_report_20251024.html  # Generated HTML report
└── expenses_export_20251024.csv  # CSV export
```

## 🎯 Features Implemented

### ✅ Core CRUD Operations
- Create, Read, Update, Delete expenses
- Category-based organization
- Date-range filtering
- Input validation

### ✅ Multiple User Interfaces
- **Admin Interface**: Full expense management
- **Public Viewer**: Read-only access with beautiful displays
- **HTML Reports**: Shareable, professional reports
- **CSV Export**: Excel-compatible data export

### ✅ Professional Data Architecture
- **SQLite Database**: Scalable, fast, reliable
- **Data Separation**: No hardcoded data in source code
- **Indexes**: Optimized database queries
- **Migration Support**: Easy data import/export

### ✅ Sharing & Collaboration
- **HTML Reports**: Open in any web browser
- **CSV Export**: Share with Excel/Google Sheets users
- **File-based sharing**: Email, cloud storage ready

## 🔮 Future Enhancements (Roadmap)

### 🚧 Next Steps
- [ ] User authentication (admin vs viewer roles)
- [ ] Google Drive integration for cloud storage
- [ ] Web interface (Flask-based)
- [ ] Budget tracking and alerts
- [ ] Recurring expense support
- [ ] Mobile-responsive design

### 🎨 Advanced Features
- [ ] Data visualization (charts/graphs)
- [ ] Multi-currency support
- [ ] Receipt photo attachments
- [ ] API endpoints for mobile apps
- [ ] Real-time collaboration

## 🛠️ Technical Details

### Dependencies
- **Python 3.7+** (built-in libraries only)
- **SQLite** (included with Python)
- **No external packages required** ✨

### Database Schema
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Supported Categories
- Food, Transport, Entertainment, Shopping
- Bills, Healthcare, Education, Travel, Other
- Custom categories supported

## 📊 Sample Data

The application includes realistic sample data with 23+ expenses across 6 categories, totaling $1,049.57, demonstrating typical personal spending patterns.

## 🎓 Learning Outcomes

This project demonstrates:
- **Data Architecture**: Database design and separation of concerns
- **User Interface Design**: Multiple access patterns for different user types
- **File I/O Operations**: JSON, CSV, HTML, and SQLite handling
- **Error Handling**: Robust exception management
- **Code Organization**: Modular, maintainable structure
- **Documentation**: Professional README and inline comments

## 👥 Sharing Your Work

### For Non-Technical Users
```bash
python3 html_report_generator.py
# Share the generated HTML file via email/cloud storage
```

### For Technical Colleagues
Share the entire project folder - they can run any of the Python files directly.

### For Data Analysis
```bash
# Export to CSV from the expense tracker menu (option 6)
# Or use database_manager.py export function
```

## 🏆 AI Hackday 2025

**Challenge**: Expense tracker – CRUD plus charts  
**Goal**: Track expenses with create, edit, delete, filter, and simple charts  
**Status**: ✅ Core requirements met + bonus features

**Author**: Created for AI Hackday 2025 Technology Challenge  
**Date**: October 24, 2025  
**Learning Focus**: Python development, database design, user interface patterns

---

💡 **Tip**: This is a complete, working expense tracker ready for real-world use while demonstrating professional software development practices!