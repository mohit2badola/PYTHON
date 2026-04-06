class vehical:
    def __init__(self,name):
        self.name=name

    def start(self):
        print(f"{self.name} is starting ")

    def fueltype(self):
        print("Generic Fuel")

class car(vehical):
    def __init__(self,name,brand):
        super().__init__(name)
        self.brand=brand

    def fueltype(self):
        print(f"{self.name }runs on Petrol/Diesel")

    def start(self):
        print(f"{self.brand} car start with a key or button")

class bike(vehical):
    def __init__(self,name,cc):
        super().__init__(name)
        self.cc=cc

    def fueltype(self):
        print(f"{self.name }runs on Petrol")

    def start(self):
        print(f"{self.name} car start with self-start/kick")


vehicles=[
    car("car1","Toyota"),
    bike("bike1",200)
]

for v in vehicles:
    v.start()
    v.fueltype()



