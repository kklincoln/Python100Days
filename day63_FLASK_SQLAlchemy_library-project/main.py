from flask import Flask, render_template, request, redirect, url_for
#ensure the requirements folder has been installed; including flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# create the app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Base class used for declarative class definitions. Essentially using a "preset" for the class of the table structure
class Base(DeclarativeBase):
  pass

# Requirements:
# configure the SQLite database, relative to the app instance folder;connection string that tells SQLAlchemy what db to connect to.
# Create an SQLite database called new-books-collection.db. Remember to initialise the app.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
# create the extension
db = SQLAlchemy(model_class=Base)
# db=SQLAlchemy()
# initialize the app with the extension
db.init_app(app)



# Create book class to create a table in this database called books.
class Book(db.Model):
# The books table should contain 4 fields: id, title, author and rating.
# ':' used for explicitly declaring a variable type.
# SQLAlchemy uses the generic Mapped so that it can type check the data that will be stored in the database.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Provide the Flask "app context" and create the 'books' schema in the database. (triggers the create_all for the class above)
with app.app_context():
    db.create_all()

# CRUD: CREATE A RECORD // Again, with the flask app context, create a new entry in the books table consisting of the following data:
# with app.app_context():
#     new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()
#     # db.session.close()

#read all records for use in the index.html file
# with app.app_context():
#     # When we execute a query during a database session we get back the rows in the database (a Result object)
#     result = db.session.execute(db.select(Book).order_by(Book.title))
#     # We then use scalars() to get the individual elements rather than entire rows.
#     all_books = result.scalars()


# CRUD: READ A RECORD// finding a particular record
# with app.app_context():
#     # note the use of scalar instead of scalars for the singular object
#     book = db.session.execute(db.select(Book).where(Book.title="Harry Potter")).scalar()

# CRUD: UPDATE A RECORD//
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
#     book_to_update.title = "Harry Potter and the Chamber of Secrets"
#     db.session.commit()
#     db.session.close()

# CRUD: DELETE A RECORD //
# with app.app_context():
#     book_to_delete = db.session.execute(db.select(Book).where(Book.title == "Harry Potter and the Chamber of Secrets")).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)
#     db.session.delete(book_to_delete)
#     db.session.commit()
#     db.session.close()

# all_books = [] # used in the example before creation of SQLite db
@app.route('/')
def home():
    #passing in the all_books list in as an argument to be used in the forloop within the index.html file
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    # We then use scalars() to get the individual elements rather than entire rows.
    return render_template("index.html", books=all_books) #,books=all_books) #used in the example before the SQLite db


@app.route("/add", methods=["GET","POST"])
def add():
    #add the script to add the book to the database; make sure to use the request.method == "POST"
    if request.method == "POST":
        # create a record using the book class
        # Print the form data to check if it's coming through correctly
        print("Form data received:", request.form)  # Print the full form data
        new_book = Book(
            # gather the info from the form in the add.html page
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        # with the db session, add the book entered
        db.session.add(new_book)
        db.session.commit()
        # db.session.close()
        # reroute back to the homepage after the book added.
        return redirect(url_for("home"))
    #if the request != "POST" load the add.html page
    return render_template("add.html")

@app.route('/edit', methods=["GET" , "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD using the id from the form
        book_id = request.form["id"]
        # get the book to update from the table Book, where id= book_id
        book_to_update = db.get_or_404(Book, book_id)
        # take the element in the edit.html called "rating" and feed it into the book_to_update
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    # when loading the edit page, using the id from the request.argument from edit.html: url_for('edit', id=book.id)
    book_id = request.args.get('id')
    # load data from the Book table, using the id from the form above
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)

@app.route('/delete')
def delete():
    #using the arguments generated from the index.html delete button
    book_id = request.args.get('id')
    #delete record by id populated from above, within the Book table
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

