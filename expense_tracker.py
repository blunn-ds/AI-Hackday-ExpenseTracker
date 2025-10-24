#!/usr/bin/env python3
"""
Personal Expense Tracker
=========================

A simple expense tracking application for the AI Hackday challenge.
Perfect for someone with library and information science background - 
focuses on data organization, categorization, and reporting.

Author: Created for AI Hackday 2025
Date: October 24, 2025
"""

# Import necessary libraries
import json         # For saving/loading data
import csv          # For CSV export functionality  
import datetime     # For handling dates
from typing import List, Dict, Optional  # For better code documentation

# Color codes for better terminal display (optional, for nice formatting)
class Colors:
    """Terminal color codes for better user interface"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # End color
    BOLD = '\033[1m'

def print_colored(text: str, color: str = Colors.ENDC) -> None:
    """Helper function to print colored text"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(text: str) -> None:
    """Print a formatted header"""
    print_colored(f"\n{'='*50}", Colors.CYAN)
    print_colored(f"{text.center(50)}", Colors.BOLD + Colors.HEADER)
    print_colored(f"{'='*50}", Colors.CYAN)

# Expense data structure
class Expense:
    """
    Represents a single expense record.
    
    This is like a 'catalog card' in library science - it contains
    all the metadata needed to describe and organize an expense.
    """
    
    def __init__(self, amount: float, category: str, description: str, date: str = None):
        """
        Initialize a new expense record
        
        Args:
            amount: The cost of the expense (e.g., 15.99)
            category: Category like 'Food', 'Transport', 'Entertainment'
            description: Brief description (e.g., 'Coffee at Starbucks')
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        self.amount = float(amount)
        self.category = category.title()  # Capitalize first letter
        self.description = description
        self.date = date if date else datetime.date.today().strftime('%Y-%m-%d')
        self.id = f"{self.date}_{len(description)}_{int(amount*100)}"  # Simple unique ID
    
    def to_dict(self) -> Dict:
        """Convert expense to dictionary for saving to file"""
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount,
            'category': self.category,
            'description': self.description
        }
    
    def __str__(self) -> str:
        """String representation for displaying"""
        return f"{self.date} | ${self.amount:6.2f} | {self.category:15} | {self.description}"

# Main ExpenseTracker class - like the library catalog system
class ExpenseTracker:
    """
    Main expense tracking system.
    
    Think of this as your personal financial catalog system - 
    it organizes, stores, and helps you find your expense records.
    """
    
    def __init__(self, data_file: str = "expenses.json"):
        """
        Initialize the expense tracker
        
        Args:
            data_file: File to save/load expenses (default: expenses.json)
        """
        self.expenses: List[Expense] = []
        self.data_file = data_file
        self.categories = {
            'Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 
            'Healthcare', 'Education', 'Travel', 'Other'
        }
        
        # Try to load existing data
        self.load_expenses()
        
        # Add sample data if no expenses exist (for demo purposes)
        if len(self.expenses) == 0:
            self.add_sample_data()
    
    def add_sample_data(self) -> None:
        """Add comprehensive sample expenses for demonstration purposes"""
        sample_expenses = [
            # Food expenses
            {
                'amount': 4.50,
                'category': 'Food',
                'description': 'Morning coffee at local cafe',
                'date': '2025-10-22'
            },
            {
                'amount': 12.75,
                'category': 'Food',
                'description': 'Lunch at downtown restaurant',
                'date': '2025-10-20'
            },
            {
                'amount': 8.25,
                'category': 'Food',
                'description': 'Pizza delivery for dinner',
                'date': '2025-10-18'
            },
            {
                'amount': 15.60,
                'category': 'Food',
                'description': 'Brunch with friends',
                'date': '2025-10-19'
            },
            
            # Shopping expenses
            {
                'amount': 67.89,
                'category': 'Shopping',
                'description': 'Weekly groceries at supermarket',
                'date': '2025-10-21'
            },
            {
                'amount': 45.99,
                'category': 'Shopping',
                'description': 'New book and stationery supplies',
                'date': '2025-10-17'
            },
            {
                'amount': 89.50,
                'category': 'Shopping',
                'description': 'Winter jacket from clothing store',
                'date': '2025-10-16'
            },
            {
                'amount': 23.75,
                'category': 'Shopping',
                'description': 'Household cleaning supplies',
                'date': '2025-10-23'
            },
            
            # Transport expenses
            {
                'amount': 15.00,
                'category': 'Transport',
                'description': 'Bus fare for city center trip',
                'date': '2025-10-24'
            },
            {
                'amount': 35.60,
                'category': 'Transport',
                'description': 'Taxi ride to airport',
                'date': '2025-10-15'
            },
            {
                'amount': 25.00,
                'category': 'Transport',
                'description': 'Weekly metro pass',
                'date': '2025-10-14'
            },
            {
                'amount': 42.30,
                'category': 'Transport',
                'description': 'Uber rides (3 trips)',
                'date': '2025-10-20'
            },
            
            # Entertainment expenses
            {
                'amount': 18.50,
                'category': 'Entertainment',
                'description': 'Movie tickets for evening show',
                'date': '2025-10-19'
            },
            {
                'amount': 32.00,
                'category': 'Entertainment',
                'description': 'Concert tickets',
                'date': '2025-10-13'
            },
            {
                'amount': 12.99,
                'category': 'Entertainment',
                'description': 'Streaming service subscription',
                'date': '2025-10-01'
            },
            {
                'amount': 28.75,
                'category': 'Entertainment',
                'description': 'Bowling night with colleagues',
                'date': '2025-10-22'
            },
            
            # Bills expenses
            {
                'amount': 125.00,
                'category': 'Bills',
                'description': 'Monthly electricity bill',
                'date': '2025-10-05'
            },
            {
                'amount': 85.50,
                'category': 'Bills',
                'description': 'Internet and cable package',
                'date': '2025-10-03'
            },
            {
                'amount': 45.00,
                'category': 'Bills',
                'description': 'Mobile phone bill',
                'date': '2025-10-07'
            },
            {
                'amount': 95.75,
                'category': 'Bills',
                'description': 'Water and gas utilities',
                'date': '2025-10-10'
            },
            
            # Healthcare expenses
            {
                'amount': 75.00,
                'category': 'Healthcare',
                'description': 'Doctor consultation',
                'date': '2025-10-12'
            },
            {
                'amount': 24.95,
                'category': 'Healthcare',
                'description': 'Prescription medication',
                'date': '2025-10-13'
            },
            {
                'amount': 120.00,
                'category': 'Healthcare',
                'description': 'Dental cleaning appointment',
                'date': '2025-10-08'
            }
        ]
        
        print_colored("Adding comprehensive sample data for demonstration...", Colors.CYAN)
        for expense_data in sample_expenses:
            expense = Expense(
                amount=expense_data['amount'],
                category=expense_data['category'],
                description=expense_data['description'],
                date=expense_data['date']
            )
            self.expenses.append(expense)
        
        # Save the sample data
        self.save_expenses()
        print_colored(f"✓ Added {len(sample_expenses)} sample expenses across multiple categories", Colors.GREEN)
        
        # Show category breakdown
        categories = {}
        for expense in self.expenses:
            categories[expense.category] = categories.get(expense.category, 0) + 1
        
        print_colored("Sample data breakdown:", Colors.BLUE)
        for category, count in sorted(categories.items()):
            print_colored(f"  • {category}: {count} expenses", Colors.CYAN)
    
    def get_categories(self) -> List[str]:
        """Get list of available categories (sorted)"""
        return sorted(list(self.categories))
    
    # CRUD Operations (Create, Read, Update, Delete)
    
    def add_expense(self, amount: float, category: str, description: str, date: str = None) -> bool:
        """
        Add a new expense to the tracker
        
        Args:
            amount: Cost of the expense
            category: Category (Food, Transport, etc.)
            description: What was purchased
            date: Date in YYYY-MM-DD format (optional, defaults to today)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate amount
            if amount <= 0:
                print_colored("Error: Amount must be positive!", Colors.FAIL)
                return False
            
            # Add category if it's new
            if category.title() not in self.categories:
                self.categories.add(category.title())
            
            # Create and add expense
            expense = Expense(amount, category, description, date)
            self.expenses.append(expense)
            
            # Save to file
            self.save_expenses()
            
            print_colored(f"✓ Added expense: ${amount:.2f} for {category}", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"Error adding expense: {e}", Colors.FAIL)
            return False
    
    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses (sorted by date, newest first)"""
        return sorted(self.expenses, key=lambda x: x.date, reverse=True)
    
    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """Get expenses filtered by category"""
        return [exp for exp in self.expenses if exp.category.lower() == category.lower()]
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Expense]:
        """Get expenses within a date range (YYYY-MM-DD format)"""
        return [exp for exp in self.expenses 
                if start_date <= exp.date <= end_date]
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense by ID"""
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                removed = self.expenses.pop(i)
                self.save_expenses()
                print_colored(f"✓ Deleted expense: {removed.description}", Colors.GREEN)
                return True
        
        print_colored("Error: Expense not found!", Colors.FAIL)
        return False
    
    # Data Persistence Methods
    
    def save_expenses(self) -> None:
        """Save all expenses to JSON file"""
        try:
            data = [expense.to_dict() for expense in self.expenses]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print_colored(f"Error saving expenses: {e}", Colors.FAIL)
    
    def load_expenses(self) -> None:
        """Load expenses from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
            for item in data:
                expense = Expense(
                    amount=item['amount'],
                    category=item['category'], 
                    description=item['description'],
                    date=item['date']
                )
                self.expenses.append(expense)
                self.categories.add(expense.category)
                
            print_colored(f"✓ Loaded {len(self.expenses)} expenses from {self.data_file}", Colors.GREEN)
            
        except FileNotFoundError:
            print_colored(f"No existing data file found. Starting fresh!", Colors.CYAN)
        except Exception as e:
            print_colored(f"Error loading expenses: {e}", Colors.FAIL)
    
    def export_to_csv(self, filename: str = None) -> bool:
        """Export expenses to CSV file"""
        if not filename:
            filename = f"expenses_export_{datetime.date.today().strftime('%Y%m%d')}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['date', 'amount', 'category', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for expense in self.get_all_expenses():
                    writer.writerow({
                        'date': expense.date,
                        'amount': expense.amount,
                        'category': expense.category,
                        'description': expense.description
                    })
            
            print_colored(f"✓ Exported {len(self.expenses)} expenses to {filename}", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"Error exporting to CSV: {e}", Colors.FAIL)
            return False
    
    # Analysis and Reporting Methods
    
    def get_total_spending(self) -> float:
        """Get total amount spent"""
        return sum(expense.amount for expense in self.expenses)
    
    def get_category_totals(self) -> Dict[str, float]:
        """Get spending totals by category"""
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        return category_totals
    
    def get_monthly_total(self, year: int, month: int) -> float:
        """Get total spending for a specific month"""
        month_str = f"{year:04d}-{month:02d}"
        return sum(expense.amount for expense in self.expenses 
                  if expense.date.startswith(month_str))
    
    def display_expenses(self, expenses: List[Expense] = None) -> None:
        """Display expenses in a formatted table"""
        if expenses is None:
            expenses = self.get_all_expenses()
        
        if not expenses:
            print_colored("No expenses to display.", Colors.WARNING)
            return
        
        print_colored(f"\n{'Date':<12} {'Amount':<8} {'Category':<15} {'Description'}", Colors.BOLD)
        print_colored("-" * 60, Colors.CYAN)
        
        total = 0
        for expense in expenses:
            print(expense)
            total += expense.amount
        
        print_colored("-" * 60, Colors.CYAN)
        print_colored(f"Total: ${total:.2f}", Colors.BOLD + Colors.GREEN)

# User Interface Functions

def show_menu() -> None:
    """Display the main menu options"""
    print_header("Main Menu")
    print_colored("1. Add Expense", Colors.GREEN)
    print_colored("2. View All Expenses", Colors.BLUE)
    print_colored("3. View by Category", Colors.BLUE)
    print_colored("4. Monthly Summary", Colors.CYAN)
    print_colored("5. Category Analysis", Colors.CYAN)
    print_colored("6. Export to CSV", Colors.WARNING)
    print_colored("7. Delete Expense", Colors.FAIL)
    print_colored("0. Exit", Colors.HEADER)
    print()

def get_user_input(prompt: str, input_type: type = str, validation_func=None):
    """Get validated user input"""
    while True:
        try:
            user_input = input(f"{prompt}: ").strip()
            if not user_input and input_type != str:
                print_colored("This field cannot be empty!", Colors.WARNING)
                continue
                
            converted_input = input_type(user_input) if user_input else ""
            
            if validation_func and not validation_func(converted_input):
                continue
                
            return converted_input
            
        except ValueError:
            print_colored(f"Please enter a valid {input_type.__name__}!", Colors.FAIL)
        except KeyboardInterrupt:
            print_colored("\n\nOperation cancelled.", Colors.WARNING)
            return None

def add_expense_interactive(tracker: ExpenseTracker) -> None:
    """Interactive function to add a new expense"""
    print_header("Add New Expense")
    
    # Get amount
    amount = get_user_input("Enter amount", float, lambda x: x > 0)
    if amount is None:
        return
    
    # Show categories and get selection
    categories = tracker.get_categories()
    print_colored("\nAvailable categories:", Colors.CYAN)
    for i, cat in enumerate(categories, 1):
        print_colored(f"{i}. {cat}", Colors.BLUE)
    print_colored(f"{len(categories) + 1}. Create new category", Colors.GREEN)
    
    cat_choice = get_user_input("Choose category (number)", int, 
                               lambda x: 1 <= x <= len(categories) + 1)
    if cat_choice is None:
        return
    
    if cat_choice <= len(categories):
        category = categories[cat_choice - 1]
    else:
        category = get_user_input("Enter new category name", str)
        if not category:
            return
    
    # Get description
    description = get_user_input("Enter description", str)
    if not description:
        return
    
    # Get date (optional)
    print_colored("\nPress Enter for today's date, or enter date (YYYY-MM-DD):", Colors.CYAN)
    date_input = input("Date: ").strip()
    
    # Add the expense
    tracker.add_expense(amount, category, description, date_input if date_input else None)

def view_by_category_interactive(tracker: ExpenseTracker) -> None:
    """Interactive function to view expenses by category"""
    categories = tracker.get_categories()
    if not categories:
        print_colored("No categories found!", Colors.WARNING)
        return
    
    print_header("View by Category")
    for i, cat in enumerate(categories, 1):
        print_colored(f"{i}. {cat}", Colors.BLUE)
    
    choice = get_user_input("Choose category (number)", int, 
                           lambda x: 1 <= x <= len(categories))
    if choice is None:
        return
    
    selected_category = categories[choice - 1]
    expenses = tracker.get_expenses_by_category(selected_category)
    
    print_header(f"Expenses in '{selected_category}'")
    tracker.display_expenses(expenses)

def monthly_summary_interactive(tracker: ExpenseTracker) -> None:
    """Show monthly spending summary"""
    print_header("Monthly Summary")
    
    year = get_user_input("Enter year", int, lambda x: 2000 <= x <= 2030)
    if year is None:
        return
        
    month = get_user_input("Enter month (1-12)", int, lambda x: 1 <= x <= 12)
    if month is None:
        return
    
    total = tracker.get_monthly_total(year, month)
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    print_colored(f"\n{month_names[month]} {year} Total: ${total:.2f}", Colors.GREEN)
    
    # Show expenses for that month
    start_date = f"{year:04d}-{month:02d}-01"
    end_date = f"{year:04d}-{month:02d}-31"
    monthly_expenses = tracker.get_expenses_by_date_range(start_date, end_date)
    
    if monthly_expenses:
        print_header("Expenses this month")
        tracker.display_expenses(monthly_expenses)

def category_analysis_interactive(tracker: ExpenseTracker) -> None:
    """Show spending analysis by category"""
    print_header("Category Analysis")
    
    category_totals = tracker.get_category_totals()
    total_spending = tracker.get_total_spending()
    
    if not category_totals:
        print_colored("No expenses recorded yet!", Colors.WARNING)
        return
    
    print_colored(f"{'Category':<15} {'Amount':<10} {'Percentage':<10}", Colors.BOLD)
    print_colored("-" * 40, Colors.CYAN)
    
    # Sort categories by spending (highest first)
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_categories:
        percentage = (amount / total_spending) * 100 if total_spending > 0 else 0
        print_colored(f"{category:<15} ${amount:<9.2f} {percentage:<9.1f}%", Colors.BLUE)
    
    print_colored("-" * 40, Colors.CYAN)
    print_colored(f"{'TOTAL':<15} ${total_spending:<9.2f} {'100.0%':<10}", Colors.BOLD + Colors.GREEN)

def delete_expense_interactive(tracker: ExpenseTracker) -> None:
    """Interactive function to delete an expense"""
    expenses = tracker.get_all_expenses()
    if not expenses:
        print_colored("No expenses to delete!", Colors.WARNING)
        return
    
    print_header("Delete Expense")
    print_colored("Recent expenses:", Colors.CYAN)
    
    # Show last 10 expenses with numbers
    recent_expenses = expenses[:10]
    for i, expense in enumerate(recent_expenses, 1):
        print_colored(f"{i}. {expense}", Colors.BLUE)
    
    choice = get_user_input("Choose expense to delete (number)", int, 
                           lambda x: 1 <= x <= len(recent_expenses))
    if choice is None:
        return
    
    selected_expense = recent_expenses[choice - 1]
    
    # Confirm deletion
    print_colored(f"\nAre you sure you want to delete:", Colors.WARNING)
    print_colored(f"{selected_expense}", Colors.FAIL)
    confirm = input("Type 'yes' to confirm: ").lower().strip()
    
    if confirm == 'yes':
        tracker.delete_expense(selected_expense.id)
    else:
        print_colored("Deletion cancelled.", Colors.CYAN)

def main():
    """Main program loop"""
    print_header("Personal Expense Tracker")
    print_colored("Welcome to your personal finance organizer!", Colors.GREEN)
    print_colored("Perfect for tracking and analyzing your spending habits.", Colors.BLUE)
    
    # Create the expense tracker instance
    tracker = ExpenseTracker()
    
    print_colored(f"\nExpense tracker initialized successfully!", Colors.GREEN)
    print_colored(f"Data will be saved to: {tracker.data_file}", Colors.CYAN)
    
    while True:
        try:
            show_menu()
            choice = get_user_input("Choose an option", int, lambda x: 0 <= x <= 7)
            
            if choice is None:
                continue
            elif choice == 0:
                print_colored("\nThank you for using Expense Tracker! 💰", Colors.GREEN)
                break
            elif choice == 1:
                add_expense_interactive(tracker)
            elif choice == 2:
                print_header("All Expenses")
                tracker.display_expenses()
            elif choice == 3:
                view_by_category_interactive(tracker)
            elif choice == 4:
                monthly_summary_interactive(tracker)
            elif choice == 5:
                category_analysis_interactive(tracker)
            elif choice == 6:
                filename = input("Enter CSV filename (or press Enter for default): ").strip()
                tracker.export_to_csv(filename if filename else None)
            elif choice == 7:
                delete_expense_interactive(tracker)
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print_colored("\n\nGoodbye! 👋", Colors.GREEN)
            break
        except Exception as e:
            print_colored(f"\nAn error occurred: {e}", Colors.FAIL)
            print_colored("Please try again.", Colors.WARNING)

if __name__ == "__main__":
    main()