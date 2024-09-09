from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_SEARCH_URL ='https://api.themoviedb.org/3/search/movie'
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_DB_API_KEY=''
MOVIE_DB_API_READ_TOKEN =('')

MOVIE_DB_USERNAME=''
MOVIE_DB_PASSWORD =''

# create the app
app = Flask(__name__)
# This line sets the location 🗺️ of the database (a file named the_film_collection.db) and the type of database 🛢️(SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# This secret key is important for ensuring the security of our application, like a lock to the database
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
# Finally, we initialize SQLAlchemy tool 🔨 through our bakery, using db.init_app(app).
db = SQLAlchemy()
# This allows them to work smoothly together, like having a skilled baker who knows how to handle the oven.
db.init_app(app)


# CREATE TABLE
# Here we define the blueprint of how movie templates 🎞️ look like in our system using class BooksDb(db.Model):
class Movie(db.Model):
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    title: Mapped[str]=mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int]=mapped_column(Integer, nullable=False)
    description: Mapped[str]=mapped_column(String(500), nullable=False)
    rating: Mapped[float]=mapped_column(Float, nullable=True)
    ranking: Mapped[int]=mapped_column(Integer, nullable=True)
    review: Mapped[str]=mapped_column(String(250), nullable=True)
    img_url: Mapped[str]=mapped_column(String(250),  nullable=False)

# This line of code is used to create tables 🪧 in the database 🛢️, but only if they don't exist yet.
# It tells the application to temporarily use the "app" context, which is necessary for communicating with the database 🛢️.
with app.app_context():
    # This line of code checks whether the tables 🪧🪧🪧 in the database 🛢️ are already created.
    # This code runs only once‼️, e.g., during the first installation of the application.
    db.create_all()


    # # Add a new movie, only if it doesn't exist in the database
    if not Movie.query.filter_by(title="Phone Booth").first():
        new_movie = Movie(
            title="Phone Booth",
            year="2002",
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
                        "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller "
                        "leads to a jaw-dropping climax.",
            rating=7.3,
            ranking=10,
            review="Two hours stuck in a phone booth, can you imagine the cast they'd need in order to make this entertaining?",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
        )
        db.session.add(new_movie)

    # # Add a new movie, only if it doesn't exist in the database
    if not Movie.query.filter_by(title="Avatar The Way of Water").first():
        second_movie = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.3,
            ranking=9,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )
        # Add the new movie to the session and commit changes
        db.session.add(second_movie)
    # commit the place of hte new movie
    db.session.commit()


#Create the edit form
class RateMovieForm(FlaskForm):
    rating = StringField(label='Your Rating Out of 10. E.g. 8.4', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField('Update Rating')

class AddMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

@app.route("/", methods=["GET"])
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() #converts the ScalarResults to a python list

    for i in range(len(all_movies)):
        #since the above is ordered by rating, the ranking for the movie is = length of movies - position
        all_movies[i].ranking = len(all_movies) - i
    #update the db to reflect the correct ranking
    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=["GET","POST"])
def edit():
    form = RateMovieForm()
    # from the index.html, when you click the edit button, an id is passed through as an argument within the URL_FOR func
    form_movie_id=request.args.get("id")
    movie=db.get_or_404(Movie,form_movie_id)
    #if form has been submitted and passes validator checks, convert the data where applicable from the form and update db
    if form.validate_on_submit():
        #update movie record
        movie.rating=float(form.rating.data)
        movie.review=form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    #if request.method != POST, load the edit page using the movie from the index.html url_for func and the form above
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete")
def delete():
    #delete the record from the database
    form_movie_id=request.args.get("id")
    movie_to_delete=db.get_or_404(Movie,form_movie_id)
    db.session.delete(movie_to_delete)
    print(f"Deleted {movie_to_delete}: {movie_to_delete.title}!")
    db.session.commit()
    #refresh the homepage without the record
    return redirect(url_for('home'))


@app.route("/add", methods=["GET","POST"])
def add():
    form = AddMovieForm()
    #if the user clicks the submit button and the validators clear, pass in the movie_title from the form into the API
    if form.validate_on_submit():
        movie_title = form.title.data
        #API_KEY and "query" are the only two required parameters for the API to function and return results
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


# when a movie is selected on selec.html, find the movie data from the API call; will be used to add into the database
@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        #the url is found in the api_docs main page, gathers data for the specific row, when provided with api key
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        # using the specific movie_api_id (record id from the API call generated in the select page)
        # call the API again for the specific movie, passing parameters for the API key
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )

        #adds the data gathered from the API call to the db as a new record
        db.session.add(new_movie)
        db.session.commit()

        #redirect to the edit page since it is missing the rating and review portion to be completed
        return redirect(url_for("edit", id=new_movie.id))


@app.route("/select")
def select():
    return render_template("select.html")

if __name__ == '__main__':
    app.run(debug=True)
