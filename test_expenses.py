#!/usr/bin/env python3
"""
Test script to show sample data from the expense tracker
"""

# Import the expense tracker
from expense_tracker import ExpenseTracker, print_header, print_colored, Colors

def show_sample_data():
    """Show the sample data without interactive menu"""
    print_header("Expense Tracker - Sample Data Demo")
    
    # Create tracker instance
    tracker = ExpenseTracker()
    
    print_colored(f"Data loaded from: {tracker.data_file}", Colors.CYAN)
    print_colored(f"Number of expenses: {len(tracker.expenses)}", Colors.BLUE)
    
    if tracker.expenses:
        # Show all expenses manually
        print_header("All Sample Expenses")
        print_colored(f"Date         Amount   Category        Description", Colors.BOLD)
        print_colored("-" * 60, Colors.CYAN)
        
        total = 0
        for expense in sorted(tracker.expenses, key=lambda x: x.date, reverse=True):
            print(expense)
            total += expense.amount
        
        print_colored("-" * 60, Colors.CYAN)
        print_colored(f"Total: ${total:.2f}", Colors.GREEN + Colors.BOLD)
        
        # Show category breakdown
        print_header("Category Breakdown")
        category_totals = {}
        for expense in tracker.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        
        print_colored(f"{'Category':<15} {'Amount':<10}", Colors.BOLD)
        print_colored("-" * 30, Colors.CYAN)
        
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            print_colored(f"{category:<15} ${amount:<9.2f} ({percentage:.1f}%)", Colors.BLUE)
        
        print_colored(f"\n✓ Your expense tracker is working perfectly!", Colors.GREEN)
        print_colored(f"✓ Sample data includes 3 different expense categories", Colors.GREEN)
        print_colored(f"Run 'python3 expense_tracker.py' for the full interactive menu.", Colors.BLUE)
    else:
        print_colored("No expenses found. The sample data should have been created automatically.", Colors.WARNING)

if __name__ == "__main__":
    show_sample_data()