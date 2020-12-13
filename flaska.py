
from flask import Flask, jsonify, request


import Process_payment
app= Flask(__name__)
@app.route("/api", methods=["POST"])
def setName():
    if request.method=='POST':
        posted_data = request.get_json()



        credit_card_number = posted_data['credit_card_number']
        card_holder = posted_data['card_holder']
        expiry_date = posted_data['expiry_date']
        security_code = posted_data['security_code']
        amount = posted_data['amount']
        expensive_payment_available = posted_data['expensive_payment_available']
        premium_payment_available = posted_data['premium_payment_available']

        api_call(credit_card_number,card_holder,expiry_date,security_code,amount,expensive_payment_available,premium_payment_available)
        return jsonify(str("Successfully stored  " + str(credit_card_number)+" " + str(card_holder)+" "+str(expiry_date)+ " "+str(security_code)+" " +str(amount)+" " +str(expensive_payment_available) +" " +str(premium_payment_available)))
@app.route("/api", methods=["POST"])
def api_call(credit_card_number,card_holder,expiry_date,security_code,amount,expensive_payment_available,premium_payment_available):

    Process_payment.Payment(credit_card_number,card_holder,expiry_date,security_code,amount,expensive_payment_available,premium_payment_available).processpayment()





if __name__=='__main__':
   app.run(debug=True)

