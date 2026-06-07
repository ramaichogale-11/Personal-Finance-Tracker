from datetime import datetime

while True:
    print("\n--- Personal Finance Tracker ---")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Total Spending")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        expense_name = input("Enter expense name: ")
        amount = float(input("Enter amount: "))

        today = datetime.now().strftime("%d-%m-%Y")

        with open("expenses.txt", "a") as file:
            file.write(f"{today}, {expense_name}, {amount}\n")

        print("Expense Saved!")

    elif choice == "2":
        print("\nExpense History:")

        with open("expenses.txt", "r") as file:
            print(file.read())

    elif choice == "3":
        total = 0

        with open("expenses.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) == 3:
                    amount = float(parts[2])
                    total = total + amount

                elif len(parts) == 2:
                    amount = float(parts[1])
                    total = total + amount

        print(f"\nTotal Spending: ₹{total}")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")