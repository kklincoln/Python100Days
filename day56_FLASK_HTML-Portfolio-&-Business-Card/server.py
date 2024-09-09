from flask import Flask, render_template

#name of curr directory
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("KiernanLincolnPage.html")

if __name__ == "__main__":
    app.run(debug=True)