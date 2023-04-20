from flask import Flask, request, render_template
import apis.finnhub_requests

import firebase_admin
from firebase_admin import credentials, auth, db

import json

f = open("SECRET.json")
data = json.load(f)


app = Flask(__name__)
cred = credentials.Certificate("firebase_key.json")


firebase_admin.initialize_app(cred, {
   'databaseURL': data["firebase_address"]
})

ref = db.reference('/')
values = ref.get()

#testing deployment
def user_stock_info(object):
    #key = TICKER
    #Value = VALUE OF STOCK, QUANTITY 
    net_worth = 0
    rv = {}
    assets = object["assets"]
    for key, value in assets.items():
        quantity = ""
        if (key == 'cash'):
            net_worth += round(value, 2)
            value = round(value, 2)
            rv[key] = (value , "N/A")
            continue
        #find price of stock
        stock_info = json.loads(apis.finnhub_requests.get_realtime_stock_data(key.upper()))
        price = stock_info['c']
        net_worth += price * value
        rv[key] = (round(price * value, 2), int(value))
    print(rv)
    return net_worth, rv

@app.route("/")
def start():
    message = None
    return render_template("signin.html", message=message)

@app.route("/signin", methods = ["GET", "POST"])
def signin():
    if(request.method == "GET"):
        return render_template("signin.html")
    elif(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        ref = db.reference('users/')
        message = None
        if(username in ref.get() and password == ref.get()[username]["password"]):
            user_object = ref.get()[username]
            net_worth, new_obj = user_stock_info(user_object)
            return render_template("dash.html", username = username, info=new_obj, net_worth=net_worth)
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
            message = "success"
        else:
            message = "Account already found"
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
@app.route("/purchase", methods = ["POST"])
def purchase():
    message = None
    stock_symbol = request.form['stock_symbol'].upper()
    quantity = float(request.form['quantity'])
    username = request.form['username']
    stock_info = json.loads(apis.finnhub_requests.get_realtime_stock_data(stock_symbol.upper()))
    if(stock_info['d'] == None):
        print("Stock cannot be found")
        message = "Stock cannot be found"
        ref = db.reference("/users/")
        user_object = ref.get()[username]
        net_worth, new_obj = user_stock_info(user_object)
        return render_template("dash.html", message=message, username=username, info=new_obj, net_worth = net_worth)
    price = float(stock_info['c'])
    data = db.reference('users/').get()
    cash = float(data[username]["assets"]["cash"])
    
    if (cash >= price * quantity):
        cash -= price * quantity
        #check if stock alr exists with user
        if stock_symbol in data[username]["assets"]:
            quantity += data[username]["assets"][stock_symbol]
        ref = db.reference("/users/")
        ref.child(username).child("assets").update({"cash": cash, stock_symbol: quantity})
    else:
        ref = db.reference("/users/")
        message = "You do not have enough cash to purchase this stock"

    user_object = ref.get()[username]
    net_worth, new_obj = user_stock_info(user_object)
    return render_template("dash.html",message=message, username = username, info=new_obj, net_worth=net_worth)


@app.route("/sell", methods = ["POST"])
def sell():
    message = None
    stock_symbol = request.form['stock_symbol'].upper()
    quantity = float(request.form['quantity'])
    username = request.form['username']
    stock_info = json.loads(apis.finnhub_requests.get_realtime_stock_data(stock_symbol.upper()))
    data = db.reference('users/').get()
    if(stock_info['d'] == None):
        print("Stock cannot be found")
        message = "Stock cannot be found"
        ref = db.reference("/users/")
        user_object = ref.get()[username]
        net_worth, new_obj = user_stock_info(user_object)
        return render_template("dash.html", message=message, username=username, info=new_obj, net_worth = net_worth)
    if (stock_symbol not in data[username]["assets"]):
        print("You don't own this stock")
        message = "You don't own this stock"
        ref = db.reference("/users/")
        user_object = ref.get()[username]
        net_worth, new_obj = user_stock_info(user_object)
        return render_template("dash.html", message=message, username=username, info=new_obj, net_worth = net_worth) 

    price = float(stock_info['c'])
    cash = float(data[username]["assets"]["cash"])
    
    cash += price * quantity
    quantity = data[username]["assets"][stock_symbol] - quantity
    if quantity == 0:
        ref = db.reference("/users/")
        stock = ref.child(username).child("assets").child(stock_symbol)
        stock.delete()
        ref.child(username).child("assets").update({"cash": cash})
    elif quantity < 0:
        print("You do not own enough of this stock")
        message = "You do not own enough of this stock"
        ref = db.reference("/users/")
        user_object = ref.get()[username]
        net_worth, new_obj = user_stock_info(user_object)
        return render_template("dash.html", message=message, username=username, info=new_obj, net_worth = net_worth)
    else:
        ref = db.reference("/users/")
        ref.child(username).child("assets").update({"cash": cash, stock_symbol: quantity})

    user_object = ref.get()[username]
    net_worth, new_obj = user_stock_info(user_object)
    return render_template("dash.html",message=message, username = username, info=new_obj, net_worth=net_worth)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/<path:path>')
def catch_all(path):
    return render_template("404.html", path=path)



if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)

