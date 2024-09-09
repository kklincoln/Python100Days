from flask import Flask, render_template
import requests

posts= requests.get(url="https://api.npoint.io/046e947e1641d39af786").json()
print(posts)
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html", all_posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

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
    app.run(debug=True)