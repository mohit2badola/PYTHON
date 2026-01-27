a=121
b=a
c=0
while b>0:
    c+=a%10
    a=int(a/100)
if(c==b):
    print("Palindreome")
else:
    print("Not palindrome")