"""
Python 3.6 or newer required.
"""
import stripe
import os

# This is a placeholder - it should be replaced with your secret API key.
# Sign in to see your own test API key embedded in code samples.
# Don’t submit any personally identifiable information in requests made with this key.
stripe.api_key = 'sk_INSERT_YOUR_SECRET_KEY'

stripe.api_version = '2023-10-16'

from flask import Flask, jsonify, send_from_directory, request

app = Flask(__name__, static_folder='src',
  static_url_path='', template_folder='src')

@app.route('/account_link', methods=['POST'])
def create_account_link():
    try:
        connected_account_id = request.get_json().get('account')

        account_link = stripe.AccountLink.create(
          account=connected_account_id,
          return_url=f"http://localhost:4242/return/{connected_account_id}",
          refresh_url=f"http://localhost:4242/refresh/{connected_account_id}",
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

@app.route('/', defaults={'path': ''})

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
    app.run()
