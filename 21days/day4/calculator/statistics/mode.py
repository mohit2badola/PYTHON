from collections import Counter

def mode(data):
    freq=Counter(data)
    return freq.most_common(1)[0][0]
    