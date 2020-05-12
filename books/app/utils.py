# from src.models.books import Book
# import src.models.books as m

from app.models import Book
from app import db

import logging as lg 


def test_intersection(set_a, set_b):
    intersection = set_a.intersection(set_b) 
    return intersection == set_a



def get_book_year_by_name(book_name, Book):
    books = Book.query.filter(Book.name == book_name).all()
    book = books[0]
    return str(book.year)

def get_books():
    books = Book.query.all()
    books = [m.serialize() for m in books]
    return books

def get_book(book_id):
    book = db.session.query(Book).get(book_id)
    # return book.serialize()
    return book




def add_book(book_name, year):
    book = Book(book_name, year)
    db.session.add(book)
    db.session.commit()
    # books = Book.query.filter(Book.id == book.id)
    # return db.session.query(Book).get(book.id).serialize()
    return db.session.query(Book).get(book.id)




def delete_book_by_id(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    db.session.delete(book)
    db.session.commit()

def update_book_by_id(book_id,book_name,book_year):
    x = db.session.query(Book).get(book_id)
    x.name = book_name
    x.year = book_year
    db.session.commit()
    # return x.serialize()
    return x
