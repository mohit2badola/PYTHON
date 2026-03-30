class bankaccount:
    def __init__ (self, account_holder,balance=0):
        self.account_holder=account_holder
        self.balance=balance

    def deposit(self,amount):
        if amount>0:
            self.balance+=amount
            print(f"{amount} deposited sucessfully")
        else:
            print(f"Invalid deposit amount")


    def withdrew(self,amount):
        if amount>0:
            self.balance-=amount
            print(f"{amount } withdrewn sucessfully")
        else:
            print("Invalid Amount")

    def checkbalance(self):
        print(f"Balance : {self.balance}")


acc1=bankaccount("Mohit",10000)

acc1.deposit(500)
acc1.checkbalance()

acc1.withdrew(320)
acc1.checkbalance()