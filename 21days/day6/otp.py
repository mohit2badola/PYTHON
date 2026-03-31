import random
import time 

class OTPSystem:
    def __init__(self):
        self.otp=None
        self.generated_time=None

    def generate_otp(self):
        self.otp=random.randint(100000,999999)
        self.generated_time=time.time()

        print(f"Generated OTP : {self.otp}")

    def varify_otp(self,user_otp):
        if self.otp is None:
            print("No OTP Generated")
            return
        current_time=time.time()

        if current_time-self.generated_time>30:
            print("OTP Expired")
            return

        if user_otp==self.otp:
            print("OTP Verified")

        else:
            print("Invalid OTP")


otp_system=OTPSystem()
otp_system.generate_otp()

user_input=int(input("Enter 6 digit otp "))

otp_system.varify_otp(user_input)

        