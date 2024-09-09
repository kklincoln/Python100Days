import wtforms.validators
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5 #pip install bootstrap-flask

# 	It must have an email and password field; They can both  StringFields; You don't have to worry about validators.
class LoginForm(FlaskForm):
    email = StringField(label='Email',validators =[DataRequired(),
        # add Email validation to the email field so that you must type a valid email (with "@" and ".") otherwise you get an error.
        Email(message=None, granular_message=False, check_deliverability=True, allow_smtputf8=True, allow_empty_local=False)])
    password = PasswordField(label='Password', validators=[DataRequired(),
        # Also add Length validation to the password, so you must type at least 8 characters.
        Length(min=8, max=30, message="Field must be at least 8 characters long.")])
        #obscures the text typed into the textbox
    login_btn = SubmitField(label='Log In')

app = Flask(__name__)
app.secret_key = "krohg34gjw0ioepmi203"
bootstrap = Bootstrap5(app) #initialize bootstrap-flask

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET","POST"])
def login():
    # create a new instance of the class for LoginForm
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Update the /login route in main.py so that if the form was submitted and validated and their credentials matched the following:
        if login_form.email.data == "admin@email.com" and login_form.password.data =="12345678":
            # then show them the success.html page.
            return render_template("success.html")
        else:
            # Otherwise show them the denied.html page
            return render_template("denied.html")
    #be sure to render the login_form alongside the login page
    return render_template('login.html', form=login_form)


@app.route('/success')
def success():
    #create a new instance to login at successful page
    return render_template("success.html")

@app.route('/denied')
def denied():
    return render_template("denied.html")


if __name__ == '__main__':
    app.run(debug=True)
