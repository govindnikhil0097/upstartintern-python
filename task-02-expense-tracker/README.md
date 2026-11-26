# Expense Tracker (Task 02)

A command-line Python script to record daily expenses, validate inputs, view spending totals by category, and export records to a spreadsheet-ready CSV file (`expenses.csv`).

## How to Run

1. Make sure Python 3.10+ is installed.
2. Clone this repository and navigate into the task folder:
   ```bash
   git clone https://github.com/govindnikhil0097/upstartintern-python.git
   cd upstartintern-python/task-02-expense-tracker
   ```
3. Run the script:
   ```bash
   python expense_tracker.py
   ```

## Design Decisions

- **Standard Library Only:** Used `csv`, `datetime`, and `os` so the script runs immediately with zero third-party dependencies.
- **Dictionary-Based Rows:** Used `csv.DictReader` and `csv.DictWriter` so each row maps cleanly to `{"date", "category", "amount"}`.
- **Input Validation:** Dates are strictly checked against `YYYY-MM-DD` using `datetime.strptime`, and amounts must be positive numbers before saving.
- **Category Normalization:** Category names are standardized with `.title()` so entries like `food` and `Food` group together accurately in category totals.
