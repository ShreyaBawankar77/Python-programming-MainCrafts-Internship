import csv
import os
from datetime import date
from collections import defaultdict

FILE_NAME = "expenses.csv"
CATEGORIES = ["Food", "Travel", "Shopping", "Health", "Entertainment", "Education", "Other"]


def initialize_file():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Category"])
        print(f"Created new expense file: {FILE_NAME}\n")


def choose_category():
    """Display category options and return the user's choice."""
    print("\nSelect a category:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")
    while True:
        try:
            choice = int(input("Enter category number: ").strip())
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print(f"Please enter a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def add_expense():
    """Prompt the user for expense details (with category) and save to CSV."""
    print("\n--- Add Expense ---")
    description = input("Enter expense description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Enter amount (e.g. 250.00): ").strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    category = choose_category()
    today = date.today().strftime("%Y-%m-%d")

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, description, f"{amount:.2f}", category])

    print(f"✔ Expense '{description}' of {amount:.2f} [{category}] added successfully!")


def load_expenses():
    """Load all expenses from CSV and return as a list of dicts."""
    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)


def print_expense_table(rows, title="All Expenses"):
    """Print a formatted table of expenses."""
    print(f"\n--- {title} ---")
    if not rows:
        print("No expenses found.")
        return

    print(f"{'#':<4} {'Date':<12} {'Description':<25} {'Category':<15} {'Amount':>10}")
    print("-" * 70)
    for i, row in enumerate(rows, start=1):
        print(f"{i:<4} {row['Date']:<12} {row['Description']:<25} {row['Category']:<15} {float(row['Amount']):>9.2f}")
    print("-" * 70)


def view_expenses():
    """Display all saved expenses."""
    rows = load_expenses()
    print_expense_table(rows)
    return rows


def search_by_category():
    """Search and display expenses filtered by category."""
    print("\n--- Search by Category ---")
    category = choose_category()
    rows = load_expenses()
    filtered = [r for r in rows if r["Category"].lower() == category.lower()]
    print_expense_table(filtered, title=f"Expenses in '{category}'")

    if filtered:
        total = sum(float(r["Amount"]) for r in filtered)
        print(f"Total for '{category}': {total:.2f}  ({len(filtered)} expense(s))")


def view_total_by_category():
    """Display total spending grouped by category."""
    print("\n--- Total Spent per Category ---")
    rows = load_expenses()

    if not rows:
        print("No expenses recorded yet.")
        return

    totals = defaultdict(float)
    counts = defaultdict(int)
    for row in rows:
        cat = row["Category"]
        totals[cat] += float(row["Amount"])
        counts[cat] += 1

    print(f"\n{'Category':<20} {'Expenses':>10} {'Total Spent':>14}")
    print("-" * 46)
    grand_total = 0
    for cat in sorted(totals):
        print(f"{cat:<20} {counts[cat]:>10} {totals[cat]:>13.2f}")
        grand_total += totals[cat]
    print("-" * 46)
    print(f"{'GRAND TOTAL':<20} {sum(counts.values()):>10} {grand_total:>13.2f}")


def view_monthly_spending():
    """Display total spending grouped by month (YYYY-MM)."""
    print("\n--- Monthly Spending ---")
    rows = load_expenses()

    if not rows:
        print("No expenses recorded yet.")
        return

    monthly = defaultdict(float)
    monthly_counts = defaultdict(int)
    for row in rows:
        month = row["Date"][:7]  # Extract YYYY-MM
        monthly[month] += float(row["Amount"])
        monthly_counts[month] += 1

    print(f"\n{'Month':<12} {'Expenses':>10} {'Total Spent':>14}")
    print("-" * 38)
    for month in sorted(monthly):
        print(f"{month:<12} {monthly_counts[month]:>10} {monthly[month]:>13.2f}")
    print("-" * 38)
    grand = sum(monthly.values())
    print(f"{'ALL TIME':<12} {sum(monthly_counts.values()):>10} {grand:>13.2f}")


def view_total():
    """Calculate and display the total amount spent."""
    rows = load_expenses()
    if not rows:
        print("\nNo expenses to calculate.")
        return
    total = sum(float(row["Amount"]) for row in rows)
    print(f"\nTotal Amount Spent: {total:.2f}  ({len(rows)} expense(s))")


def delete_expense():
    """Delete a specific expense by its number."""
    print("\n--- Delete Expense ---")
    rows = view_expenses()

    if not rows:
        return

    try:
        choice = int(input("\nEnter the expense number to delete (0 to cancel): "))
        if choice == 0:
            return
        if choice < 1 or choice > len(rows):
            print("Invalid number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    removed = rows.pop(choice - 1)

    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Description", "Amount", "Category"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Deleted: '{removed['Description']}' [{removed['Category']}] - {float(removed['Amount']):.2f}")


def main():
    """Main loop - display menu and handle user choices."""
    initialize_file()

    print("=" * 45)
    print("   Python CLI Expense Tracker 2.0")
    print("=" * 45)

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search by Category")
        print("4. View Total per Category")
        print("5. View Monthly Spending")
        print("6. View Total Spent")
        print("7. Delete an Expense")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_by_category()
        elif choice == "4":
            view_total_by_category()
        elif choice == "5":
            view_monthly_spending()
        elif choice == "6":
            view_expenses()
            view_total()
        elif choice == "7":
            delete_expense()
        elif choice == "8":
            print("\nGoodbye! Keep tracking your expenses.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
