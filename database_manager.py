#!/usr/bin/env python3
"""
SQLite Database Manager for Expense Tracker
===========================================

Proper database implementation using SQLite.
This separates data from code and provides real database capabilities.

Benefits over JSON:
- SQL queries for complex filtering
- Better performance with large datasets  
- Relationships between tables
- Data integrity constraints
- Concurrent access support
"""

import sqlite3
import datetime
from typing import List, Dict, Optional
from expense_tracker import Expense, print_colored, Colors

class ExpenseDatabaseManager:
    """
    Professional database manager for expenses.
    
    Think of this as your digital library catalog system - 
    structured, searchable, and scalable.
    """
    
    def __init__(self, db_path: str = "expenses.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Create database tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create expenses table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create categories table (for future use)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        color TEXT DEFAULT '#3498db',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_expenses_date 
                    ON expenses(date)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_expenses_category 
                    ON expenses(category)
                """)
                
                conn.commit()
                print_colored(f"✅ Database initialized: {self.db_path}", Colors.GREEN)
                
        except Exception as e:
            print_colored(f"❌ Database initialization error: {e}", Colors.FAIL)
    
    def add_expense(self, expense: Expense) -> bool:
        """Add a single expense to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO expenses (date, amount, category, description)
                    VALUES (?, ?, ?, ?)
                """, (expense.date, expense.amount, expense.category, expense.description))
                
                conn.commit()
                print_colored(f"✅ Added expense: ${expense.amount:.2f} for {expense.category}", Colors.GREEN)
                return True
                
        except Exception as e:
            print_colored(f"❌ Error adding expense: {e}", Colors.FAIL)
            return False
    
    def get_all_expenses(self) -> List[Expense]:
        """Retrieve all expenses from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, amount, category, description 
                    FROM expenses 
                    ORDER BY date DESC
                """)
                
                expenses = []
                for row in cursor.fetchall():
                    expense = Expense(
                        date=row[0],
                        amount=row[1], 
                        category=row[2],
                        description=row[3]
                    )
                    expenses.append(expense)
                
                print_colored(f"📊 Retrieved {len(expenses)} expenses from database", Colors.BLUE)
                return expenses
                
        except Exception as e:
            print_colored(f"❌ Error retrieving expenses: {e}", Colors.FAIL)
            return []
    
    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """Get expenses filtered by category"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, amount, category, description 
                    FROM expenses 
                    WHERE category = ?
                    ORDER BY date DESC
                """, (category,))
                
                expenses = []
                for row in cursor.fetchall():
                    expense = Expense(
                        date=row[0],
                        amount=row[1],
                        category=row[2], 
                        description=row[3]
                    )
                    expenses.append(expense)
                
                return expenses
                
        except Exception as e:
            print_colored(f"❌ Error filtering by category: {e}", Colors.FAIL)
            return []
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Expense]:
        """Get expenses within a date range"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, amount, category, description 
                    FROM expenses 
                    WHERE date BETWEEN ? AND ?
                    ORDER BY date DESC
                """, (start_date, end_date))
                
                expenses = []
                for row in cursor.fetchall():
                    expense = Expense(
                        date=row[0],
                        amount=row[1],
                        category=row[2],
                        description=row[3]
                    )
                    expenses.append(expense)
                
                return expenses
                
        except Exception as e:
            print_colored(f"❌ Error filtering by date range: {e}", Colors.FAIL)
            return []
    
    def get_spending_summary(self) -> Dict:
        """Get comprehensive spending statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_expenses,
                        SUM(amount) as total_amount,
                        AVG(amount) as avg_amount,
                        MIN(date) as earliest_date,
                        MAX(date) as latest_date
                    FROM expenses
                """)
                
                total_stats = cursor.fetchone()
                
                # Category breakdown
                cursor.execute("""
                    SELECT 
                        category,
                        COUNT(*) as count,
                        SUM(amount) as total,
                        AVG(amount) as average
                    FROM expenses 
                    GROUP BY category 
                    ORDER BY total DESC
                """)
                
                category_stats = cursor.fetchall()
                
                return {
                    'total_expenses': total_stats[0] or 0,
                    'total_amount': total_stats[1] or 0,
                    'avg_amount': total_stats[2] or 0,
                    'earliest_date': total_stats[3] or 'N/A',
                    'latest_date': total_stats[4] or 'N/A',
                    'categories': [
                        {
                            'name': cat[0],
                            'count': cat[1], 
                            'total': cat[2],
                            'average': cat[3]
                        } for cat in category_stats
                    ]
                }
                
        except Exception as e:
            print_colored(f"❌ Error getting summary: {e}", Colors.FAIL)
            return {}
    
    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    print_colored(f"✅ Deleted expense ID: {expense_id}", Colors.GREEN)
                    return True
                else:
                    print_colored(f"❌ No expense found with ID: {expense_id}", Colors.WARNING)
                    return False
                    
        except Exception as e:
            print_colored(f"❌ Error deleting expense: {e}", Colors.FAIL)
            return False
    
    def migrate_from_json(self, json_file: str = "expenses.json") -> bool:
        """Migrate existing JSON data to SQLite database"""
        try:
            import json
            
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            print_colored(f"🔄 Migrating {len(data)} expenses from JSON to SQLite...", Colors.CYAN)
            
            for expense_data in data:
                expense = Expense(
                    amount=expense_data['amount'],
                    category=expense_data['category'],
                    description=expense_data['description'],
                    date=expense_data['date']
                )
                self.add_expense(expense)
            
            print_colored(f"✅ Migration complete! {len(data)} expenses moved to database", Colors.GREEN)
            return True
            
        except FileNotFoundError:
            print_colored(f"❌ JSON file not found: {json_file}", Colors.WARNING)
            return False
        except Exception as e:
            print_colored(f"❌ Migration error: {e}", Colors.FAIL)
            return False
    
    def export_to_csv(self, filename: str = None) -> bool:
        """Export database to CSV"""
        if not filename:
            filename = f"expenses_export_{datetime.date.today().strftime('%Y%m%d')}.csv"
        
        try:
            import csv
            expenses = self.get_all_expenses()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'Amount', 'Category', 'Description'])
                
                for expense in expenses:
                    writer.writerow([expense.date, expense.amount, expense.category, expense.description])
            
            print_colored(f"✅ Exported {len(expenses)} expenses to {filename}", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"❌ Export error: {e}", Colors.FAIL)
            return False

def main():
    """Test the database functionality"""
    print_colored("🗄️ Testing SQLite Database Manager", Colors.BOLD + Colors.CYAN)
    
    db = ExpenseDatabaseManager()
    
    # Try to migrate existing JSON data
    db.migrate_from_json()
    
    # Get summary statistics
    summary = db.get_spending_summary()
    
    if summary:
        print_colored(f"\n📊 Database Summary:", Colors.BOLD)
        print_colored(f"Total Expenses: {summary['total_expenses']}", Colors.BLUE)
        print_colored(f"Total Amount: ${summary['total_amount']:.2f}", Colors.BLUE)
        print_colored(f"Average: ${summary['avg_amount']:.2f}", Colors.BLUE)
        print_colored(f"Date Range: {summary['earliest_date']} to {summary['latest_date']}", Colors.BLUE)
        
        print_colored(f"\n📂 Top Categories:", Colors.BOLD)
        for cat in summary['categories'][:5]:
            print_colored(f"  {cat['name']}: ${cat['total']:.2f} ({cat['count']} expenses)", Colors.GREEN)

if __name__ == "__main__":
    main()