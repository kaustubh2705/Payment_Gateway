import re
from flask import Flask, abort
from flask_api import status
import Cheappaymentgateway
import Expensivepaymentgateway
import Premiumpaymentgateway
import datetime

app = Flask(__name__)


@app.route("/api", methods=["POST"])
class Payment:
    def __init__(self, credit_card_number, card_holder, expiry_date, security_code, amount, expensive_payment_available,premium_payment_available):
        self.credit_card_number = credit_card_number
        self.card_holder = card_holder
        expiry_date = expiry_date.split(",")
        self.expiry_date = expiry_date
        self.security_code = security_code
        self.amount = amount
        self.expensive_payment_available = expensive_payment_available
        self.premium_payment_available= premium_payment_available

    def processpayment(self):

        # Checking Mandatory Conditions
        if len(self.credit_card_number) == 0 or len(self.card_holder) == 0 or len(self.expiry_date) == 0 or len(str(self.amount)) == 0:
            print(status.HTTP_400_BAD_REQUEST)
            abort(400)

        # Credit Card Validation
        if not re.search("^[456]\d{3}(-?\d{4}){3}$", self.credit_card_number) or re.search(r"(\d)\1{3}", re.sub("-", "", self.credit_card_number)):
            print(status.HTTP_400_BAD_REQUEST)
            abort(400)

        # Expiry Date Validation
        if datetime.date(int(self.expiry_date[0]), int(self.expiry_date[1]), int(self.expiry_date[2])) < datetime.date.today():
            print(status.HTTP_400_BAD_REQUEST)
            abort(400)

        # Amount Validation
        if int(self.amount) < 0:
            print(status.HTTP_400_BAD_REQUEST)
            abort(400)

        # Security Code Validation
        if len(self.security_code) != 3 and len(self.security_code) != 0:
            print(status.HTTP_400_BAD_REQUEST)
            abort(400)

        # Data Type Validation
        if type(self.credit_card_number) != str or type(self.card_holder) != str or type(self.amount) != float or type(self.security_code) != str:
            print(status.HTTP_400_BAD_REQUEST)
            abort(400)

        if int(self.amount) <= 20:
            Cheappaymentgateway.cpg()

        if 21 <= int(self.amount) <= 500:
            if (self.expensive_payment_available).lower() == "yes":
                Expensivepaymentgateway.epg()
            else:
                Cheappaymentgateway.cpg()
        else:
            n = 0
            while(n<3):
                if Premiumpaymentgateway.ppg(self.premium_payment_available) == True:
                    print("Payment is processed using Premium Payment Gateway")
                    break
                else:

                    if n==0:
                        print("Retry 1")
                    if n==1:
                        print("Retry 2")
                    if n==2:
                        print("Retry 3")
                    n += 1
            if n == 3:
                print(status.HTTP_500_INTERNAL_SERVER_ERROR)
                abort(500)
