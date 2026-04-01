from datetime import datetime
from collections import defaultdict 

class Expenses:
    def __init__(self, amount,category,date):
        self.amount=amount
        self.category=category
        self.date=datetime.strptime(date,"%Y-%m-%d")

class ExpenseTracker:
    def __init__(self):
        self.expenses=[]

    def add_expenses(self,amount,category,date):
        expense=Expenses(amount,category,date)
        self.expenses.append(expense)

    def monthly_report(self,year,month):
        total=0
        for exp in self.expenses:
            if exp.date.year==year and exp.date.month == month:
                total+= exp.amount
        return total


    def highest_spending_category(self):
        category_total=defaultdict(int)
        for exp in self.expenses:
            category_total[exp.category]+=exp.amount

        if not category_total:
            return None

        return max(category_total, key=category_total.get)

tracker=ExpenseTracker()

tracker.add_expenses(500,"Food","2026-04-01")
tracker.add_expenses(30,"Chips","2026-04-30")
tracker.add_expenses(750,"Travel","2026-03-25")
tracker.add_expenses(800,"Food","2026-03-21")

print("April Total : ", tracker.monthly_report(2026,4))

print("Top category : ",tracker.highest_spending_category())

