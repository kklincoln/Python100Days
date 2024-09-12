from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
#-------------- Import your forms from the forms.py
from forms import CreatePostForm, RegisterUserForm, LoginUserForm,CommentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login #https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.init_app(app)
#CREATE USER_LOADER CALLBACK: used to reload the user object from the user ID stored in the session;
@login_manager.user_loader
def load_user(user_id: str):
    #Returns None if the ID is not valid.; ID will be manually removed from the session and processing continues
    return User.query.get(int(user_id))

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE ADMIN ONLY DECORATOR
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # IF id is not 1, return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


# CONFIGURE TABLES
# Create a User table for all your registered users.; UserMixin provides multiple inheritance to python
class User(UserMixin, db.Model):
    __tablename__ = "registered_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    #This will act like a List of BlogPost objects attached to each User.
    #creating the parent link to the foreign key (author_id) to the BlogPost table
    posts = relationship("BlogPost", back_populates="author")
    #Creating parent link to Comments table "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
        # Create Parent reference to the User object. The "posts" refers to the posts property in the User class.
    author: Mapped["User"] = relationship(back_populates="posts")
    # Create Foreign Key, "registered_users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("registered_users.id"))#foreignKey syntax "tablename.field"
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
        #Parent relationship to the comment table
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
        #child relationship to the parent User table
    #registered_users.id refers to the tablename of the User class
    #comments refers to the comments property in the User class
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("registered_users.id"))#foreignKey syntax "tablename.field"
    comment_author = relationship("User", back_populates="comments")
        #child relationship toward the Parent BlogPost table
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id")) #foreignKey syntax "tablename.field"
    parent_post = relationship("BlogPost", back_populates="comments")
    text: Mapped[str] = mapped_column(Text, nullable=False)


#using the context of 'app', create the tables within the db
with app.app_context():
    db.create_all()


# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

#  Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterUserForm()
    #if the form has been submitted and the validators pass, hash and salt the password, store user in db
    if form.validate_on_submit():
        # hash the password using pbkdf2:sha256 (The key derivation function & parameters.); add a salt_length of 8.
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        #Create new instance of User class with the data from the form fields
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password
        )
        # check if the user already exists in the db using the email from the form data
        existing_user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if existing_user:
            flash("User already exists. Please log in.")
            return redirect(url_for("login"))
        #log in and auth user after adding details to the database; redirect uses 'current_user'
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return  redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)


# Retrieve a user from the database based on their email; validate; login
@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #check the database for the email provided
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        #check if the user exists in the database
        if not user:
            flash("That user email does not exist, please try again.")
            return redirect(url_for("login"))
        #check stored password to see if the hashsaltpass from db (user) matches the form pass
        elif not check_password_hash(user.password, password):
            flash("Invalid password. Please try again.")
            return redirect(url_for("login"))
        #else; pass in the user results and redirect
        else:
            login_user(user)
            flash("You were successfully logged in.")
            return redirect(url_for("get_all_posts"))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    print(current_user)
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET","POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    #adding the commentForm CKEditorField
    comment_form = CommentForm()
    #only allow logged-in users to comment on posts
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to log in or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment.data,
            comment_author= current_user, #current logged in user
            parent_post =requested_post  # from the db call at the top of this function
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)


# Use admin_only decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


#  Use admin_only decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# Use admin_only decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
