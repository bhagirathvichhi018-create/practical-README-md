# Smart Expense Tracker

A beginner-friendly Python project to record expenses, summarize spending, filter records, and create charts.

## Features
- Add an expense with date, amount, category, and description.
- Validates date, positive amount, and category.
- Saves expense records in `expenses.csv`.
- Uses an `ExpenseTracker` class (OOP).
- Uses NumPy for totals, averages, highest and lowest amounts.
- Uses Pandas to load, clean, group, filter, and analyze data.
- Uses Matplotlib and Seaborn for bar, line, pie, and histogram charts.
- Generates a simple text report with monthly and category spending.

## Requirements
Python 3.10 or newer is recommended.

## Setup (Windows / VS Code)
1. Extract the ZIP file.
2. Open the extracted `Smart_Expense_Tracker_Project` folder in VS Code.
3. Open Terminal > New Terminal.
4. Install the required libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run the project:

   ```bash
   python expense_tracker.py
   ```

## If requirements.txt gives an error
Make sure your terminal is inside the project folder. Run:

```bash
dir
```

You should see `expense_tracker.py`, `expenses.csv`, `requirements.txt`, and `README.md`.

If not, use `cd` to move into the extracted project folder before installing packages.

## Dataset columns
- `Date`: expense date in YYYY-MM-DD format
- `Amount`: expense amount in rupees
- `Category`: expense category
- `Description`: short expense description

## Notes
The included `expenses.csv` contains sample data. The program will add new records to this file. You can replace the sample rows with your own data, but keep the same column names.
# practical-README-md
