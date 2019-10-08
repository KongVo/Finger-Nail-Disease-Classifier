from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import stripe
import os
import base64
import io

from flask import request
from flask import jsonify
from flask import Flask

# Define a flask app
app = Flask(__name__)

import pyrebase
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                return redirect(url_for('payment'))
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('index.html', umessage=unsuccessful)
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return render_template('index.html')
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('index.html')
    return render_template('forgot_password.html')


pub_key = ''
secret_key = ''


stripe.api_key = secret_key
@app.route('/payment')
def payment():
    return render_template('payment.html', pub_key=pub_key)

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route('/pay', methods=['POST'])
def pay():
    
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=2000,
        currency='usd',
        description='The Product'
    )

    return redirect("https://fingernail-disease-detector.onrender.com", code=302)

if __name__ == '__main__':
    # app.run(port=5002, debug=True)
    app.run(debug=True)

    # Serve the app with gevent
    #
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()