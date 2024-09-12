from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

#--------------------------------------------------------
# This "Secure Website" project covers the skills outlined below:
# Hashing and Salting (Encryption & Authentication), Flask routing and forms, WebDev, SQLAchemy DB processes,
# Webpage Navigation,
#--------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE FLASK LOGIN FOR APPLICATION
#login manager contains the code that lets the app and Flask-Login work together
# (how to load user from ID, where to send users to login, etc)
login_manager = LoginManager()
#note: the initialization requires that the secret key is set (as shown above)
login_manager.init_app(app)


#CREATE USER_LOADER CALLBACK: used to reload the user object from the user ID stored in the session;
@login_manager.user_loader
def load_user(user_id):
    #Returns None if the ID is not valid.; ID will be manually removed from the session and processing continues
    return db.get_or_404(User, user_id)


# CREATE TABLE IN DB
# Note: A Mixin is simply a way to provide multiple inheritance to Python. This is how you add a Mixin:
# class MyClass(MixinClassB, MixinClassA, BaseClass):
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        # hashing and salting the password entered by the user
        hash_and_salted_password=generate_password_hash(
            # hash the password using pbkdf2:sha256 (The key derivation function & parameters.); add a salt_length of 8.
            password=request.form.get("password"), method="pbkdf2:sha256", salt_length=8)
        # create new instance of the User class with the data provided in the form fields
        new_user = User(
            email=request.form.get("email"),
            name= request.form.get("name"),
            password=hash_and_salted_password
        )
        # check if user already exists in db using the email in the form
        existing_user = db.session.execute(db.select(User).where(User.email == request.form.get("email"))).scalar()
        if existing_user:
            flash("User already exists. Please log in.")
            return redirect(url_for("login"))
        #add the new user instance into the db
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database; redirect uses current_user
        login_user(new_user)
        return redirect(url_for("secrets"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
@app.route('/login', methods=["GET","POST"])
def login():
    # if the request button was submitted; get the email and password
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # find the user by the email provided
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        # check if the stored password hash matches the entered form password hash
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not  check_password_hash(user.password, password):
            flash('Invalid password, please try again.')
            return redirect(url_for("login"))
        else:
            # if matched, pass in the user result into the login_user method
            login_user(user)
            flash('You were successfully logged in')
            return redirect(url_for("secrets"))
    return render_template("login.html", logged_in=current_user.is_authenticated)


#only logged in users should be able to view
@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    #passing the name from the current_user logged in
    return render_template("secrets.html", name=current_user.name, logged_in=True)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for("home"), logged_in=False)


@app.route('/download', methods=["GET"])
@login_required #ensuring the login permissions protect this page
def download():
    return send_from_directory(directory='static', path="files/cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
