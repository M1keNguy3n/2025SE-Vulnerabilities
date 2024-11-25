from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import bcrypt
import user_management as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)

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
        sum_num = 0
        sum_alpha = 0
        chars = list(password)
        to_replace = ["<", ">", ";"]
        replacements = ["%3C", "%3E", "%3B"]
        char_list = list(password)
        for i in range(len(char_list)):
            if char_list[i] in to_replace:
                index = to_replace.index(char_list[i])
                char_list[i] = replacements[index]
            if char_list[i].isalpha:
                sum_alpha += 1
            if char_list[i].isnumeric:
                sum_num += 1
        if len(password) < 8 or len(password) > 12:
            return render_template("/signup.html")
        if sum_num > 4:
            return render_template("/signup.html")
        if sum_alpha > 5:
            return render_template("/signup.html")
        DoB = request.form["dob"]
        salt = bcrypt.gensalt()
        password = password.hashpw(password, salt)
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
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sum_num = 0
        sum_alpha = 0
        chars = list(password)
        for i, j in enumerate(chars):
            if not j.isalnum():
                chars[i].replace(j, j.decode(encoding = "utf-8"))
            password = ''.join(chars)
        if len(password) < 8 or len(password) > 12:
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
