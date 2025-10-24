#!/usr/bin/env python3
"""
Expense Viewer - Read-Only Interface
===================================

A clean, read-only interface for viewing expenses.
Perfect for users who need to see the data but not modify it.

This is your 'public view' - anyone can see expenses but only 
authorized users can make changes.
"""

import json
import datetime
from typing import List, Dict

# Import from our main expense tracker
from expense_tracker import Expense, ExpenseTracker, print_header, print_colored, Colors

class ExpenseViewer:
    """
    Read-only expense viewer for public access.
    
    Think of this as a 'public catalog' in library terms - 
    everyone can browse and search, but only librarians can add/edit.
    """
    
    def __init__(self, data_source: str = "expenses.json"):
        """Initialize the viewer with a data source"""
        self.data_source = data_source
        self.expenses = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load expense data from source"""
        try:
            tracker = ExpenseTracker(self.data_source)
            self.expenses = tracker.expenses
            print_colored(f"📊 Loaded {len(self.expenses)} expenses", Colors.GREEN)
        except Exception as e:
            print_colored(f"Error loading data: {e}", Colors.FAIL)
            self.expenses = []
    
    def show_dashboard(self) -> None:
        """Display a beautiful dashboard overview"""
        print_header("📊 Expense Dashboard - Read Only View")
        
        if not self.expenses:
            print_colored("No expense data available.", Colors.WARNING)
            return
        
        # Calculate summary statistics
        total_amount = sum(expense.amount for expense in self.expenses)
        num_expenses = len(self.expenses)
        avg_expense = total_amount / num_expenses if num_expenses > 0 else 0
        
        # Get date range
        dates = [expense.date for expense in self.expenses]
        min_date = min(dates)
        max_date = max(dates)
        
        # Summary box
        print_colored("┌" + "─" * 48 + "┐", Colors.CYAN)
        print_colored(f"│ {'EXPENSE SUMMARY':^46} │", Colors.BOLD + Colors.CYAN)
        print_colored("├" + "─" * 48 + "┤", Colors.CYAN)
        print_colored(f"│ Total Expenses: {num_expenses:>4}                       │", Colors.BLUE)
        print_colored(f"│ Total Amount:   ${total_amount:>8.2f}                  │", Colors.BLUE)
        print_colored(f"│ Average:        ${avg_expense:>8.2f}                  │", Colors.BLUE)
        print_colored(f"│ Date Range:     {min_date} to {max_date} │", Colors.BLUE)
        print_colored("└" + "─" * 48 + "┘", Colors.CYAN)
    
    def show_by_category(self) -> None:
        """Show expenses grouped by category"""
        print_header("📂 Expenses by Category")
        
        if not self.expenses:
            print_colored("No expenses to display.", Colors.WARNING)
            return
        
        # Group by category
        categories = {}
        for expense in self.expenses:
            if expense.category not in categories:
                categories[expense.category] = []
            categories[expense.category].append(expense)
        
        # Display each category
        for category, expenses in sorted(categories.items()):
            category_total = sum(exp.amount for exp in expenses)
            print_colored(f"\n🏷️  {category.upper()} (${category_total:.2f})", Colors.BOLD + Colors.GREEN)
            print_colored("─" * 60, Colors.GREEN)
            
            for expense in sorted(expenses, key=lambda x: x.date, reverse=True):
                date_str = expense.date
                amount_str = f"${expense.amount:>6.2f}"
                print_colored(f"  {date_str} | {amount_str} | {expense.description}", Colors.BLUE)
    
    def show_recent_expenses(self, limit: int = 10) -> None:
        """Show most recent expenses"""
        print_header(f"🕒 Recent Expenses (Last {limit})")
        
        if not self.expenses:
            print_colored("No expenses to display.", Colors.WARNING)
            return
        
        # Sort by date (most recent first)
        recent = sorted(self.expenses, key=lambda x: x.date, reverse=True)[:limit]
        
        print_colored("Date       | Amount  | Category     | Description", Colors.BOLD)
        print_colored("─" * 65, Colors.CYAN)
        
        for expense in recent:
            print_colored(
                f"{expense.date} | ${expense.amount:>6.2f} | {expense.category:<12} | {expense.description}",
                Colors.BLUE
            )
    
    def show_spending_trends(self) -> None:
        """Show simple spending analysis"""
        print_header("📈 Spending Analysis")
        
        if not self.expenses:
            print_colored("No data for analysis.", Colors.WARNING)
            return
        
        # Category breakdown
        category_totals = {}
        total_spending = 0
        
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
            total_spending += expense.amount
        
        print_colored("Category Breakdown:", Colors.BOLD)
        print_colored("─" * 40, Colors.CYAN)
        
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_spending) * 100
            bar_length = int(percentage / 2)  # Scale down for display
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            print_colored(f"{category:<12} ${amount:>8.2f} ({percentage:>5.1f}%)", Colors.GREEN)
            print_colored(f"             {bar[:30]}", Colors.BLUE)
    
    def interactive_menu(self) -> None:
        """Simple menu for the read-only viewer"""
        while True:
            print_header("💰 Expense Viewer - Read Only")
            print_colored("What would you like to view?", Colors.BLUE)
            print()
            print_colored("1. 📊 Dashboard Overview", Colors.CYAN)
            print_colored("2. 📂 Expenses by Category", Colors.CYAN)
            print_colored("3. 🕒 Recent Expenses", Colors.CYAN)
            print_colored("4. 📈 Spending Analysis", Colors.CYAN)
            print_colored("5. 🔄 Refresh Data", Colors.CYAN)
            print_colored("0. 🚪 Exit", Colors.WARNING)
            print()
            
            try:
                choice = input("Enter your choice: ").strip()
                
                if choice == '1':
                    self.show_dashboard()
                elif choice == '2':
                    self.show_by_category()
                elif choice == '3':
                    self.show_recent_expenses()
                elif choice == '4':
                    self.show_spending_trends()
                elif choice == '5':
                    print_colored("🔄 Refreshing data...", Colors.CYAN)
                    self.load_data()
                elif choice == '0':
                    print_colored("Thanks for viewing! 👋", Colors.GREEN)
                    break
                else:
                    print_colored("Please enter a valid choice (0-5)", Colors.WARNING)
                
                if choice != '0':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print_colored("\n\nThanks for viewing! 👋", Colors.GREEN)
                break
            except Exception as e:
                print_colored(f"Error: {e}", Colors.FAIL)

def main():
    """Main function to run the expense viewer"""
    viewer = ExpenseViewer()
    viewer.interactive_menu()

if __name__ == "__main__":
    main()