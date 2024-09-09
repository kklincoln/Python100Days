# Importing required libraries
from flask import Flask, render_template
import requests

# Initializing the Flask app
app = Flask(__name__)

# API endpoint for the blog data
blog_url = "https://api.npoint.io/fd95eb762b80ce502a4f"
# Fetching the blog data from the API
response = requests.get(blog_url)
all_posts = response.json()

# Home route to display all blog posts
@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)

# Route to display a specific blog post by its ID, called from within index.html
@app.route('/post/<int:num>')
def get_post(num):
    return render_template("post.html", posts=all_posts, id=num)

# Running the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)