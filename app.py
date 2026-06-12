import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
FIELDNAMES = ["Date", "Category", "Name", "Amount"]
CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment", "Savings", "Other"]


def init_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def add_expense():
    print("\nCategories:", ", ".join(CATEGORIES))
    category = input("Enter category: ").strip().title()
    if category not in CATEGORIES:
        print(f"Invalid category. Choose from: {', '.join(CATEGORIES)}")
        return
    name = input("Enter expense name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    try:
        amount = float(input("Enter amount (₹): "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Enter a positive number.")
        return

    today = datetime.now().strftime("%d-%m-%Y")
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({"Date": today, "Category": category, "Name": name, "Amount": amount})
    print(f"✓ Saved: {name} (₹{amount:.2f}) under {category}")


def read_expenses():
    with open(CSV_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def view_expenses():
    rows = read_expenses()
    if not rows:
        print("\nNo expenses recorded yet.")
        return
    print(f"\n{'Date':<14} {'Category':<16} {'Name':<25} {'Amount':>10}")
    print("-" * 68)
    for row in rows:
        print(f"{row['Date']:<14} {row['Category']:<16} {row['Name']:<25} ₹{float(row['Amount']):>9.2f}")


def view_total():
    rows = read_expenses()
    if not rows:
        print("\nNo expenses recorded yet.")
        return
    total = sum(float(r["Amount"]) for r in rows)
    print(f"\nTotal Spending: ₹{total:.2f}  ({len(rows)} expenses)")


def view_by_category():
    rows = read_expenses()
    if not rows:
        print("\nNo expenses recorded yet.")
        return
    totals = {}
    counts = {}
    for row in rows:
        cat = row["Category"]
        totals[cat] = totals.get(cat, 0) + float(row["Amount"])
        counts[cat] = counts.get(cat, 0) + 1

    grand = sum(totals.values())
    print(f"\n{'Category':<16} {'Amount':>12}  {'%':>6}  {'Count':>6}")
    print("-" * 48)
    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / grand * 100) if grand else 0
        print(f"{cat:<16} ₹{amt:>11.2f}  {pct:>5.1f}%  {counts[cat]:>6}")
    print("-" * 48)
    print(f"{'TOTAL':<16} ₹{grand:>11.2f}  {'100.0%':>6}  {len(rows):>6}")


def delete_expense():
    rows = read_expenses()
    if not rows:
        print("\nNo expenses to delete.")
        return
    print(f"\n{'#':<4} {'Date':<14} {'Category':<16} {'Name':<25} {'Amount':>10}")
    print("-" * 72)
    for i, row in enumerate(rows, 1):
        print(f"{i:<4} {row['Date']:<14} {row['Category']:<16} {row['Name']:<25} ₹{float(row['Amount']):>9.2f}")
    try:
        idx = int(input("\nEnter # to delete (0 to cancel): "))
        if idx == 0:
            return
        if not (1 <= idx <= len(rows)):
            raise ValueError
    except ValueError:
        print("Invalid selection.")
        return
    removed = rows.pop(idx - 1)
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Deleted: {removed['Name']} (₹{float(removed['Amount']):.2f})")


def main():
    init_file()
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. View Spending by Category")
        print("5. Delete an Expense")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_total()
        elif choice == "4":
            view_by_category()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1–6.")


if __name__ == "__main__":
    main()
