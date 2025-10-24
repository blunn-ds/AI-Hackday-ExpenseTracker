#!/usr/bin/env python3
"""
HTML Report Generator for Expense Tracker
==========================================

Creates beautiful, shareable HTML reports that anyone can open in a web browser.
Perfect for sharing expense data with colleagues or external users.
"""

import json
import datetime
from expense_tracker import ExpenseTracker, Expense

class HTMLReportGenerator:
    """
    Generates beautiful HTML reports from expense data.
    
    Think of this as creating a 'published report' from your catalog data -
    something you can share via email, web, or any file sharing service.
    """
    
    def __init__(self, data_source: str = "expenses.json"):
        """Initialize with data source"""
        self.data_source = data_source
        self.expenses = []
        self.load_data()
    
    def load_data(self):
        """Load expense data"""
        try:
            tracker = ExpenseTracker(self.data_source)
            self.expenses = tracker.expenses
            print(f"✓ Loaded {len(self.expenses)} expenses for report generation")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.expenses = []
    
    def generate_html_report(self, output_file: str = None) -> str:
        """Generate a complete HTML report"""
        if not output_file:
            output_file = f"expense_report_{datetime.date.today().strftime('%Y%m%d')}.html"
        
        # Calculate statistics
        total_amount = sum(exp.amount for exp in self.expenses)
        num_expenses = len(self.expenses)
        avg_expense = total_amount / num_expenses if num_expenses > 0 else 0
        
        # Get date range
        if self.expenses:
            dates = [exp.date for exp in self.expenses]
            min_date = min(dates)
            max_date = max(dates)
        else:
            min_date = max_date = "N/A"
        
        # Category analysis
        categories = {}
        for expense in self.expenses:
            categories[expense.category] = categories.get(expense.category, 0) + expense.amount
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expense Report - {datetime.date.today()}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            padding: 30px;
            margin: 20px 0;
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        
        h2 {{
            color: #34495e;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .summary-card {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .summary-card h3 {{
            margin: 0 0 10px 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            margin: 0;
        }}
        
        .expenses-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .expenses-table th {{
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .expenses-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        .expenses-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .expenses-table tr:hover {{
            background: #e8f4fd;
        }}
        
        .amount {{
            font-weight: bold;
            color: #e74c3c;
        }}
        
        .category {{
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.85em;
            display: inline-block;
        }}
        
        .category-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .category-card {{
            background: #f8f9fa;
            border-left: 5px solid #3498db;
            padding: 20px;
            border-radius: 5px;
        }}
        
        .category-card h4 {{
            margin: 0 0 15px 0;
            color: #2c3e50;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .category-amount {{
            font-size: 1.3em;
            font-weight: bold;
            color: #e74c3c;
        }}
        
        .progress-bar {{
            background: #ecf0f1;
            height: 10px;
            border-radius: 5px;
            margin: 10px 0;
            overflow: hidden;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, #3498db, #2980b9);
            height: 100%;
            border-radius: 5px;
            transition: width 0.3s ease;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #7f8c8d;
            border-top: 1px solid #ecf0f1;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .container {{ padding: 20px; }}
            .expenses-table {{ font-size: 0.9em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💰 Expense Report</h1>
        <p style="text-align: center; color: #7f8c8d; font-size: 1.1em;">
            Generated on {datetime.date.today().strftime('%B %d, %Y')}
        </p>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Expenses</h3>
                <p class="value">{num_expenses}</p>
            </div>
            <div class="summary-card">
                <h3>Total Amount</h3>
                <p class="value">${total_amount:.2f}</p>
            </div>
            <div class="summary-card">
                <h3>Average Expense</h3>
                <p class="value">${avg_expense:.2f}</p>
            </div>
            <div class="summary-card">
                <h3>Date Range</h3>
                <p class="value" style="font-size: 1.2em;">{min_date}<br>to<br>{max_date}</p>
            </div>
        </div>
        
        <h2>📊 Category Breakdown</h2>
        <div class="category-summary">
"""
        
        # Add category cards
        for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_amount) * 100 if total_amount > 0 else 0
            html_content += f"""
            <div class="category-card">
                <h4>
                    {category}
                    <span class="category-amount">${amount:.2f}</span>
                </h4>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%"></div>
                </div>
                <p style="margin: 5px 0 0 0; color: #7f8c8d;">{percentage:.1f}% of total spending</p>
            </div>
"""
        
        # Add expenses table
        html_content += f"""
        </div>
        
        <h2>📋 All Expenses</h2>
        <table class="expenses-table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add expense rows
        for expense in sorted(self.expenses, key=lambda x: x.date, reverse=True):
            html_content += f"""
                <tr>
                    <td>{expense.date}</td>
                    <td><span class="category">{expense.category}</span></td>
                    <td>{expense.description}</td>
                    <td class="amount">${expense.amount:.2f}</td>
                </tr>
"""
        
        # Close HTML
        html_content += f"""
            </tbody>
        </table>
        
        <div class="footer">
            <p>This report contains {num_expenses} expenses totaling ${total_amount:.2f}</p>
            <p>Generated by Personal Expense Tracker | AI Hackday 2025</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML report generated: {output_file}")
            print(f"📧 Share this file with anyone - they can open it in any web browser!")
            return output_file
            
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
            return None

def main():
    """Generate HTML report"""
    print("🎨 Generating shareable HTML expense report...")
    
    generator = HTMLReportGenerator()
    
    if not generator.expenses:
        print("❌ No expense data found. Run the expense tracker first to add some expenses.")
        return
    
    # Generate the report
    report_file = generator.generate_html_report()
    
    if report_file:
        print(f"""
📊 Report successfully generated!

🔗 Sharing options:
   • Email the file: {report_file}
   • Upload to Google Drive/Dropbox and share the link
   • Open locally: open {report_file}
   • Host on a website for public access

👥 Anyone can view this report - no Python or technical knowledge required!
""")

if __name__ == "__main__":
    main()