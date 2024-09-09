from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# when the POST method is called by index.html to login, this decorator is called
@app.route("/login", methods=["POST","GET"])
def receive_data():
    error = None
    # to access the form data, we will need the request method from flask module
    if request.method == "POST":
        name=request.form['name']
        password=request.form['password']
        return f"<h1>Name: {name}, Password: {password}</h1>"

if __name__ == "__main__":
    app.run(debug=True)