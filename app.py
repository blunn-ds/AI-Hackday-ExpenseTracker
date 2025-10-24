#!/usr/bin/env python3
"""
Production Web Server for Expense Tracker
==========================================

Production-ready Flask application with proper configuration
for cloud deployment (Render, Heroku, etc.)

Author: Created for AI Hackday 2025
Date: October 24, 2025
"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import datetime
from expense_tracker import ExpenseTracker, Expense

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'expense-tracker-secret-key-2025')

# Initialize expense tracker
tracker = ExpenseTracker()

@app.route('/')
def dashboard():
    """Main dashboard showing expense overview"""
    try:
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
    except Exception as e:
        app.logger.error(f"Dashboard error: {e}")
        return f"Error loading dashboard: {e}", 500

@app.route('/expenses')
def view_expenses():
    """View all expenses with filtering options"""
    try:
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
    except Exception as e:
        app.logger.error(f"View expenses error: {e}")
        return f"Error loading expenses: {e}", 500

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
    
    try:
        categories = tracker.get_categories()
        return render_template('add_expense.html', categories=categories)
    except Exception as e:
        app.logger.error(f"Add expense error: {e}")
        return f"Error loading add expense form: {e}", 500

@app.route('/analytics')
def analytics():
    """Analytics and reporting page"""
    try:
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
    except Exception as e:
        app.logger.error(f"Analytics error: {e}")
        return f"Error loading analytics: {e}", 500

@app.route('/export')
def export_data():
    """Export data in various formats"""
    return render_template('export.html')

@app.route('/export_csv')
def export_csv():
    """Export expenses to CSV"""
    try:
        filename = f"expenses_web_export_{datetime.date.today().strftime('%Y%m%d')}.csv"
        success = tracker.export_to_csv(filename)
        
        if success:
            flash(f'✅ Data exported to {filename}', 'success')
        else:
            flash('❌ Error exporting data', 'error')
        
        return redirect(url_for('export_data'))
    except Exception as e:
        app.logger.error(f"Export CSV error: {e}")
        flash(f'❌ Export error: {str(e)}', 'error')
        return redirect(url_for('export_data'))

@app.route('/api/expenses')
def api_expenses():
    """API endpoint to get all expenses as JSON"""
    try:
        expenses = tracker.get_all_expenses()
        expenses_data = [expense.to_dict() for expense in expenses]
        return jsonify(expenses_data)
    except Exception as e:
        app.logger.error(f"API expenses error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    try:
        return jsonify({
            'total_amount': tracker.get_total_spending(),
            'total_expenses': len(tracker.expenses),
            'categories': tracker.get_category_totals()
        })
    except Exception as e:
        app.logger.error(f"API stats error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_expense/<expense_id>')
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        success = tracker.delete_expense(expense_id)
        
        if success:
            flash('✅ Expense deleted successfully', 'success')
        else:
            flash('❌ Error deleting expense', 'error')
        
        return redirect(url_for('view_expenses'))
    except Exception as e:
        app.logger.error(f"Delete expense error: {e}")
        flash(f'❌ Delete error: {str(e)}', 'error')
        return redirect(url_for('view_expenses'))

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'expenses_count': len(tracker.expenses),
        'total_amount': tracker.get_total_spending()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🌐 Starting Production Expense Tracker Web Application...")
    print("📊 Loading expense data...")
    
    # Show startup info
    expenses = tracker.get_all_expenses()
    total = tracker.get_total_spending()
    print(f"✅ Loaded {len(expenses)} expenses (${total:.2f} total)")
    
    if debug:
        print(f"\n🚀 Development server starting on port {port}...")
        print(f"📱 Local access: http://localhost:{port}")
    else:
        print(f"\n🚀 Production server starting on port {port}...")
        print("🌍 Public access: Available via deployment URL")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=debug)