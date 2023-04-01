from flask import Flask, request, render_template
import apis.finnhub_requests

import firebase_admin
from firebase_admin import credentials, auth, db

import json

f = open("SECRET.json")
data = json.load(f)


app = Flask(__name__)
cred = credentials.Certificate("firebase_key.json")

# firebase_admin.initialize_app(cred)


firebase_admin.initialize_app(cred, {
   'databaseURL': data["firebase_address"]
})

ref = db.reference('/')
values = ref.get()
print(values)

#testing deployment

@app.route("/")
def start():
    test_object = {}
    test_object["name"] = "Orenj"
    test_object["age"] = 99
    return render_template("index.html", obj=test_object)

@app.route("/signin", methods = ["GET", "POST"])
def signin():
    if(request.method == "GET"):
        return render_template("signin.html")
    elif(request.method == "POST"):
        print("Received signin request")
        username = request.form["username"]
        password = request.form["password"]
        ref = db.reference('users/')
        message = None
        if(username in ref.get() and password == ref.get()[username]["password"]):
            user_object = ref.get()[username]
            return render_template("dash.html", info=user_object)
        else:
            if(username in ref.get()):
                message = "Incorrect Password. Try again!"
            else:
                message = "Username Not Found"
        return render_template("signin.html", message = message)

@app.route("/signup", methods = ["GET", "POST"])
def signup():

    if(request.method == "GET"):
        message = ""
        return render_template("signup.html", message = message)
    elif(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        ref = db.reference('users/')
        message = ""
        if(username not in ref.get()):
            ref.child(username).set({"password": password, "assets": {"cash": 100000}})
            print("ACCOUNT CREATED")
        else:
            message = "Account already found"
            print("ACCOUNT DENIED")
        return render_template("signup.html", message = message)


@app.route("/stocks", methods=["POST", "GET"])
def stocks():
    if request.method == "POST":
        stock_symbol = request.form['stock_symbol']
        stock_info = json.loads(apis.finnhub_requests.get_realtime_stock_data(stock_symbol.upper()))
        return render_template("stocks.html", stock_res=stock_info)
    else:
        temp_obj = {}
        return render_template("stocks.html", stock_res=temp_obj)

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)

