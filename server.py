from flask import Flask, render_template

app = Flask(__name__)

#testing deployment

@app.route("/")
def start():
    test_object = {}
    test_object["name"] = "Orenj"
    test_object["age"] = 99
    return render_template("index.html", obj=test_object)

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)

