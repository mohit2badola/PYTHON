import math
def std_dev(data):
    mean_val=sum(data)/len(data)
    variance=sum((x-mean_val)** 2 for x in data)/len(data)
    return math.sqrt(variance)
    