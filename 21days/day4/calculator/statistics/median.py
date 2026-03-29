def median(data):
    data=sorted(data)
    n=len(data)
    mid=n//2

    if n%2==0:
        return (data[mid-1]+data[mid])/2
    return data[mid]
