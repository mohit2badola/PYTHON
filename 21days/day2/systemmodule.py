# Question 1: System Information Tool (sys module) 
# Using sys module, create a program that displays: 
# • Python version (sys.version) 
# • Platform information (sys.platform) 
# • Maximum integer size (sys.maxsize) 
# • Command line arguments (sys.argv) - create a calculator that takes numbers as 
# command line arguments 
# • Python path (sys.path) 
# Format the output in a professional report style with clear sections and headers. 

import sys

def sysinfo():
    print("System Information")


    print("Version")
    print(sys.version)

    print("Platform")
    print(sys.version)

    print("MaxSize Integer")
    print(sys.maxsize)


    print("Path")
    for i in sys.path:
        print("->",i)
    
def calculator():
    if len(sys.argv) < 4:
        print("Enter the value in value operator value manner")
    num1=float(sys.argv[1])
    num2=float(sys.argv[3])
    operator=(sys.argv[2])   # suppose input [systemodule.py,4,+,4]

    if operator=="+":
        print(f"{num1} {operator} {num2} = {num1+num2}")
    if operator=="-":
        print(f"{num1} {operator} {num2} = {num1-num2}")
    if operator=="*":
        print(f"{num1} {operator} {num2} = {num1*num2}")
    if operator=="/":
        print(f"{num1} {operator} {num2} = {num1/num2}")

    else:
        print("Invalid Chooice")
    
sysinfo()
calculator()