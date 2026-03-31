# Create class RateLimiter:

# allow only N requests per minute
# block extra requests

# 👉 Concept: time + system design (used in APIs 🔥)

# The main goal is to:

# Allow only a limited number of requests (say N requests)
# Within a time window of 1 minute (60 seconds)
# If the limit is exceeded → block further requests


import time

class RateLimiter:
    def __init__(self,max_limits):
        self.max_limits=max_limits
        self.requests=[]

    def allow_request(self):
        current_time=time.time()
        self.requests=[t for t in self.requests if current_time-t < 60]
        if len(self.requests)<self.max_limits:
            self.requests.append(current_time)
            print("Request allowed")
        else:
            print("Too many requests(Limit exceeds)")

r=RateLimiter(4)
for i in range(7):
    r.allow_request()
    time.sleep(2)
