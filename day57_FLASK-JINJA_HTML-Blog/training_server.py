from flask import Flask, render_template
from datetime import datetime
import requests
import random

app = Flask(__name__)

@app.route('/')
def home():
    random_number = random.randint(1,10)
    curr_year = datetime.now().year
    return render_template("lesson_index.html", num=random_number, copyright_yr=curr_year)

#add the carrots around the url that will be passed as a variable; used in the APIs
@app.route("/guess/<name>")
#when the guess function goes through the rout function, it will give the func an argument for name
def guess(name):
    gender_url = f"https://api.genderize.io/?name={name}"
    gender_response = requests.get(url=gender_url)
    gender_data = gender_response.json()
    gender = gender_data["gender"]

    agify_url = f"https://api.agify.io/?name={name}"
    agify_response = requests.get(url=agify_url)
    agify_data = agify_response.json()
    age = agify_data["age"]
    return render_template("guess.html", person_name=name, person_gender=gender, person_age=age)


# returns the blog, with the <num> for the id passed in as the lesson_index.html argument during declaration
@app.route("/blog/<num>")
def get_blog(num):
    blog_url="https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(url=blog_url)
    all_posts = response.json()
    #calling the data from the npoint API and using that as an argument for the blog.html template
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run()

