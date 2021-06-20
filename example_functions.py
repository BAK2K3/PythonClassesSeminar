from flask_pymongo import ObjectId
from app import mongo


# Function for Obtaining all books
def obtain_all_books():
    return list(mongo.db.Books.find())


# Function for Adding a book
def insert_one_book(book_form):
    try:
        new_book = {
                    "title": book_form.get('title'),
                    "author": book_form.get('author'),
                    "release": book_form.get('release'),
                    "image_URL": book_form.get('image_URL'),
                    "ratings": [int(book_form.get('ratings'))]
                }
        mongo.db.Books.insert_one(new_book)
        return True

    except Exception as e:
        print(e)
        return False


# Function for deleting a book
def delete_one_book(book_id):
    mongo.db.Books.delete_one({"_id": ObjectId(book_id)})


# Function for rating a book
def add_book_rating(book_id, rating):
    try:
        book = mongo.db.Books.find_one({"_id": ObjectId(book_id)})
        book['ratings'].append(rating)
        mongo.db.Books.update_one({"_id": ObjectId(book_id)},
                                  {"$set": book})
        return True

    except Exception as e:
        print(e)
        return False


# Function for calculating average
def calculate_average(books):

    for i in range(len(books)):
        books[i]['ratings'] = round(sum(books[i]['ratings']) / len(books[i]['ratings']), 2)
    return books
