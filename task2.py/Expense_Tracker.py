import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"


def initialize_file():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount"])
        print(f"Created new expense file: {FILE_NAME}\n")


def add_expense():
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

    today = date.today().strftime("%Y-%m-%d")

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, description, f"{amount:.2f}"])

    print(f"Expense '{description}' of {amount:.2f} added successfully!")


def view_expenses():
    """Read and display all saved expenses in a formatted table."""
    print("\n--- All Expenses ---")

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("No expenses recorded yet.")
        return

    print(f"{'#':<4} {'Date':<12} {'Description':<25} {'Amount':>10}")
    print("-" * 55)

    for i, row in enumerate(rows, start=1):
        print(f"{i:<4} {row['Date']:<12} {row['Description']:<25} {float(row['Amount']):>9.2f}")

    print("-" * 55)


def view_total():
    """Calculate and display the total amount spent."""
    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("\nNo expenses to calculate.")
        return

    total = sum(float(row["Amount"]) for row in rows)
    print(f"\nTotal Amount Spent: {total:.2f}  ({len(rows)} expense(s))")


def delete_expense():
    """Delete a specific expense by its number."""
    print("\n--- Delete Expense ---")
    view_expenses()

    with open(FILE_NAME, mode="r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

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
        writer = csv.DictWriter(file, fieldnames=["Date", "Description", "Amount"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Deleted: '{removed['Description']}' - {float(removed['Amount']):.2f}")


def main():
    """Main loop - display menu and handle user choices."""
    initialize_file()

    print("=" * 40)
    print("   Python CLI Expense Tracker")
    print("=" * 40)

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spent")
        print("4. Delete an Expense")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_expenses()
            view_total()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("\nGoodbye! Keep tracking your expenses.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
