"""
Smart Expense Tracker
Beginner-friendly Python project using OOP, control structures, NumPy,
Pandas, Matplotlib, and Seaborn.
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


CSV_FILE = "Smart_Expense_Tracker_Project.csv"
CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Health", "Education", "Other"]


class ExpenseTracker:
    """Store, analyze, filter, and visualize expenses."""

    def __init__(self, filename=CSV_FILE):
        self.filename = filename
        self.columns = ["Date", "Amount", "Category", "Description"]
        self.load_data()

    def load_data(self):
        """Load expenses from CSV, or create an empty dataset."""
        if os.path.exists(self.filename):
            try:
                self.df = pd.read_csv(self.filename)
                for column in self.columns:
                    if column not in self.df.columns:
                        self.df[column] = ""
                self.df = self.df[self.columns]
                self.clean_data()
            except (pd.errors.EmptyDataError, pd.errors.ParserError):
                self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = pd.DataFrame(columns=self.columns)
            self.save_data()

    def clean_data(self):
        """Remove incomplete or invalid rows and convert data types."""
        self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
        self.df["Amount"] = pd.to_numeric(self.df["Amount"], errors="coerce")
        self.df["Category"] = self.df["Category"].astype(str).str.strip().str.title()
        self.df["Description"] = self.df["Description"].fillna("").astype(str).str.strip()
        self.df = self.df.dropna(subset=["Date", "Amount", "Category"])
        self.df = self.df[self.df["Amount"] > 0]
        self.df["Date"] = self.df["Date"].dt.strftime("%Y-%m-%d")
        self.df = self.df.reset_index(drop=True)

    def save_data(self):
        """Save the current dataset to CSV."""
        self.df.to_csv(self.filename, index=False)

    def add_expense(self, date_value, amount, category, description):
        """Validate and add one expense."""
        try:
            valid_date = datetime.strptime(date_value, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-10-13.")
            return

        try:
            amount = float(amount)
        except ValueError:
            print("Amount must be a number.")
            return

        category = category.strip().title()
        description = description.strip()

        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        if category not in CATEGORIES:
            print("Invalid category. Choose one from the category list.")
            return
        if not description:
            description = "No description"

        new_row = pd.DataFrame([{
            "Date": valid_date.strftime("%Y-%m-%d"),
            "Amount": amount,
            "Category": category,
            "Description": description
        }])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.save_data()
        print("Expense added successfully!")

    def get_summary(self):
        """Show total, average, and category-wise expense summary."""
        if self.df.empty:
            print("No expenses available yet.")
            return

        amounts = self.df["Amount"].to_numpy(dtype=float)  # NumPy array
        print("\n--- Expense Summary ---")
        print(f"Number of expenses : {len(amounts)}")
        print(f"Total spending     : Rs. {np.sum(amounts):,.2f}")
        print(f"Average expense    : Rs. {np.mean(amounts):,.2f}")
        print(f"Highest expense    : Rs. {np.max(amounts):,.2f}")
        print(f"Lowest expense     : Rs. {np.min(amounts):,.2f}")
        print("\nSpending by category:")
        print(self.df.groupby("Category")["Amount"].sum().sort_values(ascending=False).round(2).to_string())

    def filter_expenses(self, condition=None):
        """Filter expenses by category, date range, or minimum amount."""
        if self.df.empty:
            print("No expenses available to filter.")
            return

        print("\n1. Filter by category")
        print("2. Filter by date range")
        print("3. Filter by minimum amount")
        choice = input("Choose filter: ").strip()

        if choice == "1":
            category = input(f"Category {CATEGORIES}: ").strip().title()
            result = self.df[self.df["Category"] == category]
        elif choice == "2":
            start = input("Start date (YYYY-MM-DD): ").strip()
            end = input("End date (YYYY-MM-DD): ").strip()
            try:
                start_date = pd.to_datetime(start)
                end_date = pd.to_datetime(end)
                dates = pd.to_datetime(self.df["Date"])
                result = self.df[(dates >= start_date) & (dates <= end_date)]
            except ValueError:
                print("Invalid date format.")
                return
        elif choice == "3":
            try:
                minimum = float(input("Minimum amount: "))
                result = self.df[self.df["Amount"] >= minimum]
            except ValueError:
                print("Please enter a valid number.")
                return
        else:
            print("Invalid choice.")
            return

        if result.empty:
            print("No matching expenses found.")
        else:
            print(result.to_string(index=False))

    def generate_report(self):
        """Create a short report with useful metrics."""
        if self.df.empty:
            print("No data available. Add expenses first.")
            return

        monthly = self.df.copy()
        monthly["Month"] = pd.to_datetime(monthly["Date"]).dt.to_period("M").astype(str)
        total = self.df["Amount"].sum()
        category_totals = self.df.groupby("Category")["Amount"].sum()
        top_category = category_totals.idxmax()
        month_totals = monthly.groupby("Month")["Amount"].sum()

        print("\n========== SMART EXPENSE REPORT ==========")
        print(f"Total spending       : Rs. {total:,.2f}")
        print(f"Average per expense  : Rs. {self.df['Amount'].mean():,.2f}")
        print(f"Top spending category: {top_category}")
        print(f"Number of records    : {len(self.df)}")
        print("\nMonthly spending:")
        print(month_totals.round(2).to_string())
        print("\nCategory spending percentage:")
        percentage = (category_totals / total * 100).sort_values(ascending=False)
        print(percentage.round(2).astype(str).add("%").to_string())
        print("==========================================")

    def show_charts(self):
        """Display bar, line, pie, and histogram charts."""
        if self.df.empty:
            print("No data available for charts. Add expenses first.")
            return

        data = self.df.copy()
        data["Date"] = pd.to_datetime(data["Date"])
        category_totals = data.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        daily_totals = data.groupby("Date")["Amount"].sum().sort_index()

        sns.set_theme(style="whitegrid")

        # Bar chart: total spending by category
        plt.figure(figsize=(9, 5))
        sns.barplot(x=category_totals.index, y=category_totals.values)
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (Rs.)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

        # Line graph: spending over time
        plt.figure(figsize=(9, 5))
        plt.plot(daily_totals.index, daily_totals.values, marker="o")
        plt.title("Daily Spending Trend")
        plt.xlabel("Date")
        plt.ylabel("Amount (Rs.)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

        # Pie chart: category share
        plt.figure(figsize=(7, 7))
        plt.pie(category_totals.values, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        plt.title("Expense Distribution by Category")
        plt.tight_layout()
        plt.show()

        # Histogram: frequency of expense amounts
        plt.figure(figsize=(9, 5))
        sns.histplot(data["Amount"], bins=10, kde=False)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Amount (Rs.)")
        plt.ylabel("Number of Expenses")
        plt.tight_layout()
        plt.show()


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n========== SMART EXPENSE TRACKER ==========")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Expense summary")
        print("4. Filter expenses")
        print("5. Generate report")
        print("6. Show charts")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            print(f"Categories: {', '.join(CATEGORIES)}")
            date_value = input("Date (YYYY-MM-DD): ").strip()
            amount = input("Amount (Rs.): ").strip()
            category = input("Category: ").strip()
            description = input("Description: ").strip()
            tracker.add_expense(date_value, amount, category, description)
        elif choice == "2":
            if tracker.df.empty:
                print("No expenses available yet.")
            else:
                print(tracker.df.to_string(index=False))
        elif choice == "3":
            tracker.get_summary()
        elif choice == "4":
            tracker.filter_expenses()
        elif choice == "5":
            tracker.generate_report()
        elif choice == "6":
            tracker.show_charts()
        elif choice == "7":
            print("Thank you for using Smart Expense Tracker!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
