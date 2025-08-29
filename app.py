"""
Python 3.6 or newer required.
"""
import stripe
import os
import requests
import json

# This is a placeholder - it should be replaced with your secret API key.
# Sign in to see your own test API key embedded in code samples.
# Don’t submit any personally identifiable information in requests made with this key.
#stripe.api_key = os.environ['stripe']
stripe.api_key = os.environ['stripeTest']

stripe.api_version = '2023-10-16'

from flask import Flask, jsonify, send_from_directory, request, render_template

app = Flask(__name__, static_folder='public',
  static_url_path='', template_folder='public')

@app.route('/account_link', methods=['POST'])
def create_account_link():
    try:
        connected_account_id = request.get_json().get('account')

        account_link = stripe.AccountLink.create(
          account=connected_account_id,
          return_url=f"https://sample-react-rt2za.ondigitalocean.app/return/{connected_account_id}",
          refresh_url=f"https://sample-react-rt2za.ondigitalocean.app/refresh/{connected_account_id}",
          type="account_onboarding",
        )

        return jsonify({
          'url': account_link.url,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account link: ', e)
        return jsonify(error=str(e)), 500

@app.route('/account', methods=['POST'])
def create_account():
    try:
        account = stripe.Account.create()

        return jsonify({
          'account': account.id,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account: ', e)
        return jsonify(error=str(e)), 500

@app.route('/')
def hello():
    return render_template('index.html')

# Flask does not like serving static files with a sub-path, so just force them to serve up the frontend here
@app.route('/return/<path>')
@app.route('/refresh/<path>')
@app.route('/<path:path>')
def catch_all(path, **kwargs):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
  app.run(debug=True, port=8080)

@app.route('/complete', methods=['POST'])
def createCharge():
    data = json.loads(request.data)
    appID = data['appID']
    unit_amount = int(data['unit_amount'])
    acctID = data['acctID']
    try:
      session = stripe.checkout.Session.create(
      line_items=[
        {
          "price_data": {
            "currency": "usd",
            "product_data": {"name": appID},
            "unit_amount": (unit_amount * 100),
          },
          "quantity": 1,
        },
      ],
    #  payment_intent_data={"application_fee_amount": 123},
      mode="payment",
      success_url="https://sample-react-rt2za.ondigitalocean.app/success?session_id=acct_1S1B2NCArl7jXbcH",
      stripe_account= "acct_1S1B2NCArl7jXbcH",
      )
      return jsonify ({'url':'https://sample-react-rt2za.ondigitalocean.app/success?session_id=acct_1S1B2NCArl7jXbcH'})
    
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account link: ', e)
        return jsonify(error=str(e)), 500
