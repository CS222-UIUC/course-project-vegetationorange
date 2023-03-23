from flask import Flask, render_template

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
print(values)
# print("hello world")
#testing deployment

@app.route("/")
def start():
    test_object = {}
    test_object["name"] = "CS341"
    test_object["age"] = 99
    return render_template("index.html", obj=test_object)

@app.route("/signin")
def signin():
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)