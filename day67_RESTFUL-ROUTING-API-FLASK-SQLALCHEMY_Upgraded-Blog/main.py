from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
#initialize the CKEditor object
ckeditor = CKEditor()
ckeditor.init_app(app)
Bootstrap5(app)


# CREATE DATABASE WITHIN INSTANCE FOLDER
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

# WTForm: CREATE POSTS CLASS
class CreatePostForm(FlaskForm):
    title = StringField(label="Blog Post Title", validators=[DataRequired()])
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    author = StringField(label="Your Name", validators=[DataRequired()])
    bg_url = StringField(label="Blog Image URL", validators=[DataRequired()])
    # Notice body is using a CKEditorField and not a StringField; this provides the full text editor
    body = CKEditorField(label="Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


#homepage
@app.route('/')
def get_all_posts():
    # db.session.execute(db.select(...)) constructs a query to select data from the database.
    result = db.session.execute(db.select(BlogPost).order_by(BlogPost.date))
    #Convert the data to a python list;
    #You’ll usually use the Result.scalars() method to get a list of results, or the Result.scalar() method to get a single result.
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

# A route so that you can click on individual posts
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# add_new_post() to create a new blog post
@app.route('/new-post', methods=["GET","POST"])
def new_post():
    form = CreatePostForm()
    # if adding a post to the database, if validated with the information required by the class, post to db
    if form.validate_on_submit():
        # CRUD: CREATE A RECORD // Again, with the flask app context, create a new entry in the books table consisting of the following data:
        with app.app_context():
            new_post = BlogPost(
                # fields in BlogPost class: id, title, subtitle, date, body, author, img_url
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=date.today().strftime("%B %d, %Y"),# September 9, 2024
                body=form.body.data,
                author=form.author.data,
                img_url=form.bg_url.data
            )
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('get_all_posts'))
    # first load: GET request; generate the make-post.html with the form of CreatePostForm
    return render_template("make-post.html", form=form)


# edit-post() to change an existing blog post
@app.route('/edit-post/<post_id>', methods=["GET","POST"])
def edit_post(post_id):
    #db call within the table BlogPost, search for post_id
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        # Auto-populate the form fields for an existing post with the data from db call above
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        author=post.author,
        img_url=post.img_url
    )
    # Redirect the user to the blog entry after submitting their edits
    if edit_form.validate_on_submit():
        #When the user is done editing in the WTForm, they click "Submit Post", the post should now be updated in the db
        # CRUD: UPDATE A RECORD// (referring to the post field above)
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.body = edit_form.body.data
        post.author = edit_form.author.data
        post.img_url = edit_form.bg_url.data
        #note: not changing the date field; represents the original post date
        db.session.commit()
        # the user redirected to the post.html page for that blog post.
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# delete_post() to remove a blog post from the database
@app.route('/delete-post/<post_id>')
def delete_post(post_id):
    # CRUD: DELETE A RECORD //
    blog_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(blog_to_delete)
    db.session.commit()
    return redirect( url_for("get_all_posts"))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
