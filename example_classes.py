"""
Example Classes
=============

Contains the Book Class for retreiving,
storing, editing, and preparing data relating
to books stored in a DB.

Classes: Book
"""
from app import mongo
from flask_pymongo import ObjectId


class Book():
    """
    A class that represents a book.
    Performs the relevant DB functions
    along with data preperation.
    """

    # This is called whenever a class is instantiated
    def __init__(self, title, author, release, image_URL, ratings, _id=None):
        """
        Book initialisation
        """
        self._id = _id
        self.title = title
        self.author = author
        self.release = release
        self.image_URL = image_URL
        self.ratings = ratings if isinstance(ratings, list) else [int(ratings)]

    # Self-calling classes - methods of instantiated classes
    def get_info(self):
        """Formats and returns the current Book's attributes as a dict.

        The format of the dictionary allows the return of this method
        to be written directly to the Database.
        """

        info = {'title': self.title, 'author': self.author,
                'release': self.release, 'image_URL': self.image_URL,
                'ratings': self.ratings}
        return info

    def insert_into_database(self):
        """Writes a Book to the Database.

        Writes the output of the get_info
        method directly to the database.
        """
        mongo.db.Books.insert_one(self.get_info())

    def add_book_rating(self, rating):
        """Adds a rating to an existing book,
        and updated DB.
        """

        self.ratings.append(rating)
        mongo.db.Books.update_one({"_id": ObjectId(self._id)},
                                  {"$set": self.get_info()})

    def calculate_average(self):
        """
        Update the ratings field to be an average of the
        array.
        """
        self.ratings = round(sum(self.ratings) / len(self.ratings), 2)

    # Can be called without instantiating a class
    @staticmethod
    def delete_one_book(_id):
        """
        Removes a book from the database
        """
        mongo.db.Books.delete_one({"_id": ObjectId(_id)})


    @classmethod
    def obtain_one_book(cls, book_id):
        """
        Obtains a book from the database via ID
        """
        book = mongo.db.Books.find_one({"_id": ObjectId(book_id)})
        return cls(**book)

    # For methods that deal with classes as a whole
    @classmethod
    def obtain_all_books(cls):
        """
        Obtains a list of all books
        and calculates averages
        """
        data = list(mongo.db.Books.find())
        return_list = []
        if data is not None:
            for book in data:
                new_entry = cls(**book)
                new_entry.calculate_average()
                return_list.append(new_entry)
        return return_list
