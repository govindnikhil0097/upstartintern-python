import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"
FIELDNAMES = ['date', 'category', 'amount']

def loadExpenses(filename: str) -> list[dict]:
    """Load existing expenses from CSV as a list of dictionaries."""
    if not os.path.exists(filename):
        return []

    expenses = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i in reader:
            i['amount'] = float(i['amount'])
            expenses.append(i)
    return expenses

def saveExpenses(filename: str, expenses: list[dict]) -> None:
    """Write all expense dictionaries to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)

def isValidDate(date_str: str) -> bool:
    """Check if date follows YYYY-MM-DD and is a real calendar date."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def getValidExpense() -> dict:
    """Prompt user for expense details and validate date and amount."""
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        if isValidDate(date_str):
            break
        print("Invalid date. Please use YYYY-MM-DD (eg: 2026-11-26).")

    while True:
        category = input("Enter category (eg: Food, Travel, Books): ").strip()
        if category:
            category = category.title()
            break
        print("Category cannot be empty.")

    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            if amount > 0:
                break
            print("Amount must be greater than 0.")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
    return {
        "date": date_str,
        "category": category,
        "amount": round(amount, 2),
    }


def showCategoryTotals(expenses: list[dict]) -> None:
    """Calculate and display total spending grouped by category."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    totals: dict[str, float] = {}
    for i in expenses:
        cat = i['category']
        totals[cat] = totals.get(cat, 0.0) + i['amount']

    print('\n-- Spending by Category --')
    for category, total in sorted(totals.items()):
        print(f"{category:<15} : {total:.2f}")
    print(f"{'Total':<15} : {sum(totals.values()):.2f}\n")

def main() -> None:
    expenses = loadExpenses(FILE_NAME)
    while True:
        print("1. Add an expense")
        print("2. View totals by category")
        print("3. Save & Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            expense = getValidExpense()
            expenses.append(expense)
            saveExpenses(FILE_NAME, expenses)
            print("Expense validated and saved to CSV.\n")
        elif choice == '2':
            showCategoryTotals(expenses)
        elif choice == '3':
            saveExpenses(FILE_NAME, expenses)
            print(f"All records saved to {FILE_NAME}.")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3\n")

if __name__ == "__main__":
    main()

                        