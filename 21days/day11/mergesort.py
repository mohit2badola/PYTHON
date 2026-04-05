def mergesort(arr,l,m,r):
    n1=m-l+1
    n2=r-m

    L=[0]*n1
    R=[0]*n2

    for i in range(n1):

        L[i]=arr[l+i]
    for j in range(n2):
        R[j]=arr[m+1+j]

    i=j=0

    k=l

    while i<n1 and j <n2:
        if L[i]<=R[j]:
            arr[k]=L[i]
            i+=1

        else:
            arr[k]=R[j]
            j+=1

        k+=1
    while i<n1:
        arr[k] =L[i]
        i+=1
        k+=1
    while j<n2:
        arr[k] =R[j]
        j+=1
        k+=1


def mergesoting(arr,l,r):
    if l<r:
        m=(l+r)//2
        mergesoting(arr,1,m)
        mergesoting(arr,m+l,r)
        mergesort(arr,l,m,r)

arr=[32,42,63,62,62,63,63,5,2]
print(f"Given Arraya{arr}")

mergesoting(arr,0,len(arr)-1)

print(f"Sorted array is {arr}")

