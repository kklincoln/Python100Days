from flask import Flask, render_template, request
from smtplib import SMTP
import requests
import os
from dotenv import load_dotenv
load_dotenv()

posts = requests.get("https://api.npoint.io/046e947e1641d39af786").json()
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

app = Flask(__name__)

def send_email(name, email, phone, message):
    # establish SMTP commection and enable transport layer security(encryption)
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=email,
                            to_addrs=RECIPIENT_EMAIL,
                            msg=f"Subject:Contact Request from Blog Site!\n\n"
                                f"{name},({email}, {phone}) messaged via your blog site! Contents of message:\n "
                                f"{message}"
                            )

#code gathered from day59
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        sender_name = data["name"]
        sender_email = data["email"]
        sender_phone = data["phone"]
        sender_msg= data["message"]
        # send email, review day 32 for smtp practices
        send_email(sender_name, sender_email, sender_phone, sender_msg)
        return render_template("contact.html",msg_sent=True)
    return render_template("contact.html",msg_sent=False)



# int:index is a vaue that will be passed when the object is clicked/called in one of the index.html sections. (post id)
@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        # if there's a blog_post from the posts request, with the id passed as argument, then requested_post == that post
        if blog_post["id"] == index:
            requested_post = blog_post
    # return the post template with the data for the requested post
    return render_template("post.html", post=requested_post)



if __name__ == "__main__":
    app.run(debug=True, port=5001)
