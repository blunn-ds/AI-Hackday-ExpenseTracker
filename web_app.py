#!/usr/bin/env python3
"""
Web-Based Expense Tracker
=========================

Flask web application for sharing expense tracker with colleagues.
Accessible via web browser from any device on the network.

Author: Created for AI Hackday 2025
Date: October 24, 2025
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import datetime
from expense_tracker import ExpenseTracker, Expense
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'expense-tracker-secret-key-2025'  # For flash messages

# Initialize expense tracker
tracker = ExpenseTracker()

@app.route('/')
def dashboard():
    """Main dashboard showing expense overview"""
    expenses = tracker.get_all_expenses()
    total_amount = tracker.get_total_spending()
    category_totals = tracker.get_category_totals()
    
    # Get recent expenses (last 10)
    recent_expenses = expenses[:10]
    
    # Calculate some stats
    num_expenses = len(expenses)
    avg_expense = total_amount / num_expenses if num_expenses > 0 else 0
    
    # Get date range
    if expenses:
        dates = [exp.date for exp in expenses]
        min_date = min(dates)
        max_date = max(dates)
    else:
        min_date = max_date = "N/A"
    
    return render_template('dashboard.html', 
                         expenses=recent_expenses,
                         total_amount=total_amount,
                         num_expenses=num_expenses,
                         avg_expense=avg_expense,
                         min_date=min_date,
                         max_date=max_date,
                         category_totals=category_totals)

@app.route('/expenses')
def view_expenses():
    """View all expenses with filtering options"""
    category_filter = request.args.get('category', '')
    
    if category_filter:
        expenses = tracker.get_expenses_by_category(category_filter)
    else:
        expenses = tracker.get_all_expenses()
    
    categories = tracker.get_categories()
    
    return render_template('expenses.html', 
                         expenses=expenses, 
                         categories=categories,
                         selected_category=category_filter)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add new expense form"""
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            category = request.form['category']
            description = request.form['description']
            date = request.form['date'] if request.form['date'] else None
            
            success = tracker.add_expense(amount, category, description, date)
            
            if success:
                flash(f'✅ Expense added successfully: ${amount:.2f} for {category}', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('❌ Error adding expense. Please try again.', 'error')
                
        except ValueError:
            flash('❌ Invalid amount. Please enter a valid number.', 'error')
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'error')
    
    categories = tracker.get_categories()
    return render_template('add_expense.html', categories=categories)

@app.route('/analytics')
def analytics():
    """Analytics and reporting page"""
    category_totals = tracker.get_category_totals()
    total_spending = tracker.get_total_spending()
    
    # Calculate percentages for pie chart
    category_percentages = {}
    for category, amount in category_totals.items():
        percentage = (amount / total_spending) * 100 if total_spending > 0 else 0
        category_percentages[category] = {
            'amount': amount,
            'percentage': percentage
        }
    
    # Monthly data (current month)
    current_date = datetime.date.today()
    current_month_total = tracker.get_monthly_total(current_date.year, current_date.month)
    
    return render_template('analytics.html', 
                         category_percentages=category_percentages,
                         total_spending=total_spending,
                         current_month_total=current_month_total,
                         current_month=current_date.strftime('%B %Y'))

@app.route('/export')
def export_data():
    """Export data in various formats"""
    return render_template('export.html')

@app.route('/export_csv')
def export_csv():
    """Export expenses to CSV"""
    filename = f"expenses_web_export_{datetime.date.today().strftime('%Y%m%d')}.csv"
    success = tracker.export_to_csv(filename)
    
    if success:
        flash(f'✅ Data exported to {filename}', 'success')
    else:
        flash('❌ Error exporting data', 'error')
    
    return redirect(url_for('export_data'))

@app.route('/api/expenses')
def api_expenses():
    """API endpoint to get all expenses as JSON"""
    expenses = tracker.get_all_expenses()
    expenses_data = [expense.to_dict() for expense in expenses]
    return jsonify(expenses_data)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    return jsonify({
        'total_amount': tracker.get_total_spending(),
        'total_expenses': len(tracker.expenses),
        'categories': tracker.get_category_totals()
    })

@app.route('/delete_expense/<expense_id>')
def delete_expense(expense_id):
    """Delete an expense"""
    success = tracker.delete_expense(expense_id)
    
    if success:
        flash('✅ Expense deleted successfully', 'success')
    else:
        flash('❌ Error deleting expense', 'error')
    
    return redirect(url_for('view_expenses'))

if __name__ == '__main__':
    print("🌐 Starting Expense Tracker Web Application...")
    print("📊 Loading expense data...")
    
    # Show startup info
    expenses = tracker.get_all_expenses()
    total = tracker.get_total_spending()
    print(f"✅ Loaded {len(expenses)} expenses (${total:.2f} total)")
    
    print("\n🚀 Web server starting...")
    print("📱 Access from your computer: http://localhost:5000")
    print("🌍 Share with colleagues: http://YOUR_IP_ADDRESS:5000")
    print("\n💡 To find your IP address, run: ipconfig getifaddr en0")
    print("⚠️  Press Ctrl+C to stop the server")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)