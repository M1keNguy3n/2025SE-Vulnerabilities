from flask import Flask, render_template, request, redirect, url_for, session
import user_management as dbHandler
import pyotp
import pyqrcode
import os
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/index.html', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    user_secret = pyotp.random_base32() #generate the one-time passcode         
    totp = pyotp.TOTP(user_secret)
    otp_uri = totp.provisioning_uri(name=username,issuer_name="YourAppName")
    qr_code = pyqrcode.create(otp_uri)
    stream = BytesIO()
    qr_code.png(stream, scale=5)
    qr_code_b64 = base64.b64encode(stream.getvalue()).decode('utf-8')
    if request.method == 'POST':
        otp_input = request.form['otp']
        if totp.verify(otp_input):
            return redirect(url_for('home'))  # Redirect to home if OTP is valid
        else:
            return "Invalid OTP. Please try again.", 401
    return render_template('index.html')