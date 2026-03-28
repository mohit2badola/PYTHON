# Create programs using time module: 
# • Display current time using time.time(), time.ctime(), time.localtime() 
# • Format time using time.strftime() with different format codes 
# • Create countdown timer using time.sleep() 
# • Calculate age in years, months, days from birth date 
# • Find day of week for any given date 
# Display results in user-friendly format with proper labels

import time 

print ("All the time formats")
current_time=time.time()
print(f"Current time = {current_time}")

print(f"C_time= {time.ctime(current_time)}")


print(f"Local time = {time.localtime(current_time)}")


print("Structured time")

current_time=time.localtime()
print(current_time)

print(f"Time in (dd-mm-yy) =", time.strftime("%d-%m-%y", current_time))

print("time in (HH-MM-SS)", time.strftime("%H-%M-%S", current_time))

print("Day of the week", time.strftime("%A", current_time))

print("Name of the Month", time.strftime("%B",current_time))

print("Time in full format \n\n",time.strftime("%A %d %B %H:%M:%S %p",current_time))