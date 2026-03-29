from day4.calculator.basic import *
from day4.calculator.conversion import *
from day4.calculator.scientific import *
from day4.calculator.statistics import *



print("ADD", add(5,3))

print("kg to g", kg_to_g(52))

# BASIC
print("Add:", add(5, 3))
print("Sum:", sum([10, 4]))
print("Multiply:", multiply(2, 6))
print("Divide:", division(10, 2))

# SCIENTIFIC
print("Sine:", sine(0))
print("Log:", log(100, 10))
print("Power:", power(2, 3))

# STATISTICS
data = [1, 2, 2, 3, 4]
print("Mean:", mean(data))
print("Median:", median(data))
print("Mode:", mode(data))
print("Std Dev:", std_dev(data))

# CONVERSION
print("C to F:", c_to_f(0))
print("Meters to KM:", meter_to_km(1000))
print("KG to Grams:", kg_to_g(2))