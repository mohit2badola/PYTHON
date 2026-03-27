# This function or part of program will contain the utility functions which we will call in the main program

def isprime(n):
    c=0
    for i in range(1,n):
        if n%i==0:
            c+=0
    if c==1:
        print(f"The number {n} is prime")
    else:
        print(f"The number {n} is not prime")


def factorial(n):
    fact=1
    for i in range(1,n+1):
        fact*=i
    print(f"The factorial of the number {n} is {fact}")


def GCD(x,y):
    if x==0:
        return y
    return GCD(y%x ,x)


def lcm(x,y):
    def c_gcd(x,y):
        while(y):
            x,y=y,x%y
        return x
    def c_lcm(x,y):
        lc=(x*y)//c_gcd(x,y)
        return lc
    print(f"The LCM of {x} and {y} is {c_lcm(x,y)}")


def perfectnumber(n):
    sum=0
    for i in range(1,n):
        if n%i==0:
            sum+=i
    if n==sum:

        print(f"The number {n} is a Perfect number")
    else:
        print(f"The number {n} is a Perfect number")