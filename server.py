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

@app.route("/signin")
def signin():
     return render_template("signin.html")

@app.route("/signup")
def signup():
     return render_template("signup.html")


@app.route("/stocks/", methods=["POST", "GET"])
def stocks():
    if request.method == "POST":
        stock_symbol = request.form['stock_symbol']
        stock_info = json.loads(apis.finnhub_requests.get_realtime_stock_data(stock_symbol.upper()))
        print(stock_info)
        return render_template("stocks.html", stock_res=stock_info)
    else:
        temp_obj = {}
        return render_template("stocks.html", stock_res=temp_obj)

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)

