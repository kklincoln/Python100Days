import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


#initialize the extension
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# Provide the Flask "app context" and create the schema in the database.
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
# Create an SQLite database called new-books-collection.db. Remember to initialise the app.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db.init_app(app)


# Create a table in this database called books.
class User(db.Model):
# The books table should contain 4 fields: id, title, author and rating.
# The fields should have the same limitations as before e.g. INTEGER/FLOAT/VARCHAR/UNIQUE/NOT NULL etc.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)


#create table schema in the DB; requires application context
with app.app_context():
    db.create_all()

#create record
with app.app_context():
    new_book = User(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()



#////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////

#create a new connection to the sqlite db
# db = sqlite3.connect("books-collection.db", timeout= 10)
#
# #create a cursor that can control the database; i.e. a mouse-pointer
# cursor = db.cursor()
#
# #create a database table, similar to a sheet in excel
# #execute tells the cursor to execute an action in SQL commands
#  # table: id | title | author | rating
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
#
# db.commit()
