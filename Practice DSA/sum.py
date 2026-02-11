l=[1,2,3,4,5,6,7,8,9]
target=8

for i in range(len(l)-1):
    for j in range(i,len(l)):
        if (l[i]+l[j])==target:
            print(i,j)
            

