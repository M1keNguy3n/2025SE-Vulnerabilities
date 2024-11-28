from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import bcrypt
import user_management as dbHandler
import helper as h
import pyotp
import pyqrcode
import os
import base64
from io import BytesIO
# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.secret_key = 'supersecurekey'
# no rate limiter #
# no csp #
@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
# too many methods #
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        feedback = h.sanitize(feedback)
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else: #catchall, no exception handling#
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")

# no rate limiter #
# no csp #
@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
# too many methods #
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        #sanitize here#
        username = request.form["username"]
        password = request.form["password"]
        username = h.sanitize(username)
        password = h.sanitize(password)
        if not h.validate(password):
            return render_template("/signup.html")
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else: #catchall, no exception handling#
        return render_template("/signup.html")

# no rate limiter #
# no csp #
@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
# too many methods #
@app.route("/", methods=["POST", "GET"])
def home():
    user_secret = pyotp.random_base32()
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        username = h.sanitize(username)
        password = h.sanitize(password)
        if not h.validate(password):
            return render_template("/index.html")
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else: #catchall, no exception handling#
            return render_template("/index.html")
    else: #catchall, no exception handling#
        return render_template("/index.html")

# debug mode #
if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
