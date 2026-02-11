def countdown(num):
    if num==0:
        print("Times UP")
        print()
        return
    print(num)
    countdown(num-1)