import csv
import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class Expense:
    def __init__(self, amount, category, date, description):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description


class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.budget = 0
        self.load_data()

    def add_expense(self):
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = datetime.now().strftime("%Y-%m-%d")

            exp = Expense(amount, category, date, description)
            self.expenses.append(exp)

            print("Expense added!")

        except ValueError:
            print(" Invalid input!")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses found.")
            return

        print("\n--- Expenses ---")
        for e in self.expenses:
            print(f"{e.date} | {e.category} | ₹{e.amount} | {e.description}")

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"💰 Total Spent: ₹{total}")

        if self.budget:
            print(f"📊 Budget: ₹{self.budget}")
            print(f"Remaining: ₹{self.budget - total}")

    def set_budget(self):
        try:
            self.budget = float(input("Enter budget: "))
            print(" Budget set!")
        except ValueError:
            print(" Invalid input!")

    def save_data(self):
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Category", "Date", "Description"])

            for e in self.expenses:
                writer.writerow([e.amount, e.category, e.date, e.description])

        print("Data saved to CSV!")

    def load_data(self):
        if not os.path.exists("expenses.csv"):
            return

        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header

            for row in reader:
                amount, category, date, description = row
                self.expenses.append(
                    Expense(float(amount), category, date, description)
                )

    def export_pdf(self):
        if not self.expenses:
            print("No data to export.")
            return

        doc = SimpleDocTemplate("expense_report.pdf")
        elements = []
        styles = getSampleStyleSheet()

        # Title
        elements.append(Paragraph("Expense Report", styles["Title"]))

        # Table Data
        data = [["Date", "Category", "Amount", "Description"]]

        for e in self.expenses:
            data.append([e.date, e.category, f"₹{e.amount}", e.description])

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)

        doc.build(elements)

        print(" PDF exported successfully!")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spending")
        print("4. Set Budget")
        print("5. Save to CSV")
        print("6. Export to PDF")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            tracker.add_expense()

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            tracker.total_spent()

        elif choice == "4":
            tracker.set_budget()

        elif choice == "5":
            tracker.save_data()

        elif choice == "6":
            tracker.export_pdf()

        elif choice == "7":
            tracker.save_data()
            print("Exiting...")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()