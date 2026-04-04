class Book:
    library_name="Badola Library"

    def __init__(self,author,title,price):
        self.title=title
        self.author=author
        self.__price=price   #__(double underscore) means private variable

    def display(self):
        print(f"Book {self.title} by  {self.author}")

    def get_price(self):
        return self.__price


book1=Book("Mohit","Python Basics",300)
book2=Book("Rishabh","ALL ABOUT ITCS",1500)

book1.display()
print("Price:",book1.get_price())

book2.display()
print("Library:",Book.library_name)
