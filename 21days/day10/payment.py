from abc import ABC,abstractmethod
class payment(ABC):
    @abstractmethod
    def pay(self,amount):
        pass


class cardpayment(payment):
    def pay(self,amount):
        return f"Paid Rs.{amount} using card"

    
class UPI(payment):
    def pay(self,amount):
        return f"Paid Rs.{amount} using UPI"

class bill :
    def __init__(self,amount):
        self.amount=amount

    def __str__(self):
        return f"Bill Amount: rs.{self.amount}"

    def __add__(self,other):                        #Function Overloading +
        return bill(self.amount +other.amount)

b1=bill(523)
b2=bill(3548)

print(b1)

b3=b1+b2
print(f"Total : {b3}")

payment1=cardpayment()
payment2=UPI()

print(b3)
print(payment1.pay(b2.amount))
print(payment2.pay(b1.amount))