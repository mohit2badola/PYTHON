
# Create a class ShoppingCart that:

# Stores items (name + price)
# Allows adding items
# Supports:
# len(cart) → number of items
# item in cart → check if item exists
# cart1 + cart2 → merge two carts
# print(cart) → show cart nicely

class shoppingCart:
    def __init__(self,name):
        self.name=name 
        self.item=[]

    def add_item(self,item,price):
        self.item.append((item,price))


    def __str__(self):
        return f"{self.name}'s Cart with {len(self.item)} items"

    def __repr__(self):
        return f"ShoppingCart(name={self.name}, items={self.item})"

    def __len__(self):
        return len(self.item)

    def __add__(self,other):
        new_cart=shoppingCart(self.name + " & " + other.name)

        new_cart.item=self.item + other.item

        return new_cart

    def __eq__(self,other):
        return len(self.item)==len(other.item)


    def __lt__(self,other):
        return len(self.item)<len(other.item)

    def __call__(self):
        total=sum(items[1] for items in self.item)
        return f"Total Bill : Rs. {total}"

    def __del__(self):
        # print(f"{self.name}'s cart deleted")
        pass


cart1=shoppingCart("Mohit")

cart1.add_item("Laptop", 50000)
cart1.add_item("Mouse", 500)


cart2=shoppingCart("Rishabh")
cart2.add_item("KEyboard" , 1500)


print(cart1)
print(cart2)