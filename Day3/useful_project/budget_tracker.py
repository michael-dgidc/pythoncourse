"""
Budget Tracker Project Demo

This file contains the main user interface for the budget tracker.
It allows users to:
1. Add expenses
2. Display reports
3. Export data to CSV
4. Export data to HTML
5. Exit the application
"""

# Import functions from other modules.
# data_store handles creating, loading, and saving expense data.
from data_store import create_expense, load_expenses, save_expenses

# reports handles displaying and exporting reports.
from reports import export_expenses_csv, export_expenses_html, print_report


# Dictionary used to store menu choices and their descriptions.
# The key is the option entered by the user.
# The value is the text shown in the menu.
MENU_OPTIONS = {
    "1": "Add expense",
    "2": "Display report",
    "3": "Export CSV and display in spreadsheet",
    "4": "Export HTML and display in browser",
    "5": "Exit",
}


def show_menu():
    """
    Display the menu options and ask the user to make a selection.

    Returns:
        str: The user's menu choice.
    """

    # Print menu heading.
    print("\nBudget Tracker Menu")

    # Loop through all menu options and display them.
    for key, label in MENU_OPTIONS.items():
        print(f" {key}. {label}")

    # Read user input and remove leading/trailing spaces.
    choice = input("Make your selection: ").strip()

    # Return the selected menu option.
    return choice


def get_amount():
    """
    Prompt the user to enter a valid expense amount.

    Validation rules:
    - Must be a number.
    - Must be greater than zero.

    Returns:
        float: A validated expense amount rounded to 2 decimal places.
    """

    # Keep asking until valid input is entered.
    while True:

        # Get amount from user.
        value = input("Enter the amount in dollars: ").strip()

        try:
            # Convert input string to a floating-point number.
            amount = float(value)

        except ValueError:
            # Happens if user enters text instead of a number.
            print("Amount should be entered as a number (e.g. 12.5).")
            continue

        # Check amount is positive.
        if amount <= 0:
            print("The amount entered must be more than zero.")
            continue

        # Return amount rounded to 2 decimal places.
        return round(amount, 2)


def add_expense(expenses):
    """
    Add a new expense item to the expense list.

    Args:
        expenses (list): Current list of stored expenses.
    """

    # Ask user for expense category.
    # If nothing is entered, default to "other".
    category = (
        input("Category (food, transport, bills, other): ")
        .strip()
        or "other"
    )

    # Get a validated amount.
    amount = get_amount()

    # Ask user for a description.
    # If left blank, use "N/A".
    description = input("Description: ").strip() or "N/A"

    # Create a new expense record.
    expense = create_expense(amount, category, description)

    # Add expense to the in-memory list.
    expenses.append(expense)

    # Save updated list to storage.
    save_expenses(expenses)

    # Confirm successful addition.
    print(f"Expense added: ${amount:.2f}")


def run():
    """
    Start the main budget tracker application.

    Controls the program flow and handles menu selections.
    """

    # Welcome message displayed when program starts.
    print("Welcome to the Budget Tracker project demo.")

    # Load existing expenses from storage.
    expenses = load_expenses()

    # Main application loop.
    # Continues until the user chooses Exit.
    while True:

        # Display menu and get user's choice.
        choice = show_menu()

        # Option 1: Add expense.
        if choice == "1":
            add_expense(expenses)

        # Option 2: Display report.
        elif choice == "2":
            print("Creating report...")
            print_report(expenses)

        # Option 3: Export to CSV.
        elif choice == "3":
            export_expenses_csv(expenses)

        # Option 4: Export to HTML.
        elif choice == "4":
            export_expenses_html(expenses)

        # Option 5: Exit program.
        elif choice == "5":
            print("Goodbye!")
            break

        # Handle invalid menu choices.
        else:
            print("Invalid selection. Please choose an option from 1 to 5.")


# This special condition checks whether the file is being
# run directly by Python or imported into another module.
#
# If run directly:
#     python budget_tracker.py
# then __name__ will be "__main__" and run() executes.
#
# If imported:
#     import budget_tracker
# then __name__ will be "budget_tracker" and run() will NOT execute.
#
# This prevents the program from starting automatically when imported.
if __name__ == "__main__":
    run()
