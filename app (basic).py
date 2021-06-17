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

    # books = mongo.db.Books.find()

    books = list(mongo.db.Books.find())

    for i in range(len(books)):
        books[i]['Ratings'] = round(sum(books[i]['Ratings']) / len(books[i]['Ratings']), 2)

    return render_template("index.html", books=books)


# Flask Route for adding book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    # POST Method
    if request.method == "POST":

        new_book = {
            "Title": request.form.get('title'),
            "Author": request.form.get('author'),
            "Release": request.form.get('date'),
            "Image_URL": request.form.get('urlInput'),
            "Ratings": [int(request.form.get('firstRating'))]
        }

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

    mongo.db.Books.delete_one({"_id": ObjectId(book_id)})

    # GET Method
    return redirect(url_for("index"))


# Flask Route for Adding Rating
@app.route("/rate_book/<book_id>", methods=["GET", "POST"])
def rate_book(book_id):

    book = mongo.db.Books.find_one({"_id": ObjectId(book_id)})
    book['Ratings'].append(int(request.form.get("addRating")))
    mongo.db.Books.update_one({"_id": ObjectId(book_id)},
                              {"$set": book})

    # GET Method
    return redirect(url_for("index"))


# Run the Flask Application
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port="5000",
            debug=True)
