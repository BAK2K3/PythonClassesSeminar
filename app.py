# Imports
import os
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo

# Initialise Flask App
app = Flask(__name__)

# Configure Flask
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initialise Mongo
mongo = PyMongo()
mongo.init_app(app)

# Do not recommend this for production
from example_classes import Book


# Flask Route for home
@app.route("/")
def index():

    # Obtain all books
    books = Book.obtain_all_books()
    return render_template("index.html", books=books)


# Flask Route for adding book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    # POST Method
    if request.method == "POST":

        # Create a instnace of book using form
        new_book = Book(**request.form)
        # Insert into DB
        new_book.insert_into_database()

        return redirect(url_for("index"))

    # GET Method
    return render_template("add_book.html")


# Flask Route for deleting book
@app.route("/delete_book/<book_id>")
def delete_book(book_id):

    if request.method == "POST":

        # Call static function to delete book
        Book.delete_one_book(book_id)

    # GET Method
    return redirect(url_for("index"))


# Flask Route for Adding Rating
@app.route("/rate_book/<book_id>", methods=["GET", "POST"])
def rate_book(book_id):

    if request.method == "POST":

        # Create an instance of a book using existing book id
        existing_book = Book.obtain_one_book(book_id)
        # Update the book rating
        existing_book.add_book_rating(int(request.form.get("addRating")))

    # GET method
    return redirect(url_for("index"))


# Run the Flask Application
if __name__ == "__main__":

    app.run(host="0.0.0.0",
            port="5000",
            debug=True)
