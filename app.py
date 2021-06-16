# Imports
import os
from flask import Flask, render_template, request
from flask.helpers import url_for
from flask_pymongo import PyMongo
from werkzeug.utils import redirect


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
    books = mongo.db.Books.find()
    return render_template("index.html", books=books)


# Flask Route for adding book
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    # POST Method
    if request.method == "POST":
        print(request.form)
        return redirect(url_for("index"))

    # GET Method
    return render_template("add_book.html")


# Flask Route for deleting book
@app.route("/delete_book/<book_id>")
def delete_book(book_id):

    # GET Method
    return redirect(url_for("index"))


# Flask Route for viewing book
@app.route("/view_book/<book_id>")
def view_book(book_id):

    # GET Method
    return redirect(url_for("index"))


# Run the Flask Application
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port="5000",
            debug=True)
