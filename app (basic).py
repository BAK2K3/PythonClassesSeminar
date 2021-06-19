# Imports
import os
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo, ObjectId


# Initialise Flask App
app = Flask(__name__)

# Configure Flask
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initialise Mongo
mongo = PyMongo()
mongo.init_app(app)


# Flask Route for home
@app.route("/")
def index():

    # Obtain all books from DB
    books = list(mongo.db.Books.find())

    # Loop through all books and average the ratings
    for i in range(len(books)):
        books[i]['ratings'] = round(sum(books[i]['ratings']) / len(books[i]['ratings']), 2)

    return render_template("index.html", books=books)


# Flask Route for adding book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    # POST Method
    if request.method == "POST":

        # Create a dictionary from form fields
        new_book = {
            "title": request.form.get('title'),
            "author": request.form.get('author'),
            "release": request.form.get('date'),
            "image_URL": request.form.get('urlInput'),
            "ratings": [int(request.form.get('firstRating'))]
        }

        # Insert the book into the DB
        try:
            mongo.db.Books.insert_one(new_book)
        except Exception as e:
            print(e)

        return redirect(url_for("index"))

    # GET Method
    return render_template("add_book.html")


# Flask Route for deleting book
@app.route("/delete_book/<book_id>")
def delete_book(book_id):

    # Delete a book from the DB using the requested bookID
    mongo.db.Books.delete_one({"_id": ObjectId(book_id)})

    # GET Method
    return redirect(url_for("index"))


# Flask Route for Adding Rating
@app.route("/rate_book/<book_id>", methods=["GET", "POST"])
def rate_book(book_id):

    if request.method == "POST":

        # Obtain the requested book from the DB
        book = mongo.db.Books.find_one({"_id": ObjectId(book_id)})

        # Append the new rating to the ratings list
        book['ratings'].append(int(request.form.get("addRating")))

        # Update the book entry in the DB
        mongo.db.Books.update_one({"_id": ObjectId(book_id)},
                                {"$set": book})

    # GET Method
    return redirect(url_for("index"))


# Run the Flask Application
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port="5000",
            debug=True)
