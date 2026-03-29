def add(a,b):
    return a+b

def add_multiple(*args):
    sum=0
    for i in args:
        sum+=i
    return sum
