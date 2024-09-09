from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5 #pip install bootstrap-flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

# create the new class for the form associated with adding a cafe
class CafeForm(FlaskForm):
    # make all fields required except submit
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    # add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
    # use a validator to check that the URL field has a URL entered.
    location = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField(label='Closing Time e.g. 5:30PM', validators=[DataRequired()])
    # make coffee/wifi/power a select element with choice of 0 to 5. e.g. You could use emojis ☕/💪/✘/🔌
    coffee_rating = SelectField(label='Coffee Rating', choices=["✘","☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField(label='Wifi Strength Rating', choices=["✘","💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"],
                              validators=[DataRequired()])
    power_outlet_rating = SelectField(label='Power Socket Availability', choices=["✘","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"],
                                      validators=[DataRequired()])
    submit = SubmitField('Submit')

# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
    # Make the form write a new row into cafe-data.csv
        with open("cafe-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_outlet_rating.data}" )
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
