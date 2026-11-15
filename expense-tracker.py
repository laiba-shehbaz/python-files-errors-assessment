"""Institute Expense Tracker - records daily operational expenses (stationery,
internet bills, refreshments, transport, ...) in a CSV file.

Columns in expenses.csv: date,item,category,amount
"""

import csv
import math
from datetime import date, datetime

FILENAME = "expenses.csv"
FIELDNAMES = ["date", "item", "category", "amount"]


def load_expenses(filename=FILENAME):
    """Load expenses from the CSV file. Start empty if the file does not exist."""
    expenses = []
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append(
                        {
                            "date": row["date"],
                            "item": row["item"],
                            "category": row["category"],
                            "amount": float(row["amount"]),
                        }
                    )
                except (ValueError, KeyError, TypeError):
                    print(f"  Skipped a damaged row in {filename}: {row}")
        print(f"Loaded {len(expenses)} expense(s) from {filename}.")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty expense list.")
    return expenses


def save_expenses(expenses, filename=FILENAME):
    """Write every expense to the CSV file (with a header row)."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(
                    {**expense, "amount": f"{expense['amount']:.2f}"}
                )
    except OSError as error:
        print(f"Could not save to {filename}: {error}")


def ask_amount():
    """Keep asking until the user types a valid positive number."""
    while True:
        text = input("Amount: ").strip()
        try:
            amount = float(text)
            if not math.isfinite(amount) or amount <= 0:
                raise ValueError("amount must be a positive number")
            return round(amount, 2)
        except ValueError:
            print("  Invalid amount. Please enter a positive number, e.g. 12.50")


def ask_date():
    """Ask for a date in YYYY-MM-DD format; Enter uses today's date."""
    while True:
        text = input("Date (YYYY-MM-DD, Enter for today): ").strip()
        if not text:
            return date.today().isoformat()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("  Invalid date. Use the format YYYY-MM-DD, e.g. 2026-11-02")


def ask_text(prompt):
    """Ask for non-empty text."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("  This field cannot be empty.")


def unique_categories(expenses):
    """Return the set of unique categories."""
    return {expense["category"] for expense in expenses}


def add_expense(expenses):
    print("\n--- Add New Expense ---")
    if expenses:
        print(f"Existing categories: {', '.join(sorted(unique_categories(expenses)))}")
    expense_date = ask_date()
    item = ask_text("Item: ")
    category = ask_text("Category: ").title()
    amount = ask_amount()
    expenses.append(
        {"date": expense_date, "item": item, "category": category, "amount": amount}
    )
    save_expenses(expenses)
    print(f"Saved: {item} ({category}) - {amount:.2f}")


def show_all(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"{'Date':<12}{'Item':<26}{'Category':<15}{'Amount':>10}")
    print("-" * 63)
    for e in expenses:
        print(f"{e['date']:<12}{e['item']:<26}{e['category']:<15}{e['amount']:>10.2f}")
    print("-" * 63)
    print(f"{'Total':<53}{sum(e['amount'] for e in expenses):>10.2f}")
    categories = sorted(unique_categories(expenses))
    print(f"\nUnique categories ({len(categories)}): {', '.join(categories)}")


def total_by_category(expenses):
    print("\n--- Total Expenses by Category ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    for category in sorted(totals):
        print(f"{category:<15}{totals[category]:>10.2f}")
    print("-" * 25)
    print(f"{'Grand total':<15}{sum(totals.values()):>10.2f}")


def main():
    expenses = load_expenses()
    try:
        while True:
            print("\n===== Institute Expense Tracker =====")
            print("1. Add New Expense")
            print("2. Show All Expenses")
            print("3. Calculate Total Expenses by Category")
            print("4. Exit")
            choice = input("Choose an option (1-4): ").strip()

            if choice == "1":
                add_expense(expenses)
            elif choice == "2":
                show_all(expenses)
            elif choice == "3":
                total_by_category(expenses)
            elif choice == "4":
                break
            else:
                print("  Invalid choice. Please enter 1, 2, 3 or 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed.")
    save_expenses(expenses)
    print(f"Goodbye! {len(expenses)} expense(s) saved to {FILENAME}.")


if __name__ == "__main__":
    main()
