import time


seconds=int(input("Enter the time in seconds"))

print("COUNTDOWN STARTS!!!!")

for i in range(seconds,0,-1):
    print(i)
    time.sleep(1)

print("Alert Times UPPPPP")