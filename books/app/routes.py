from app import application
from flask import Flask, render_template
from flask import jsonify, make_response
from flask import request, abort
import logging as lg 
import requests
from config import Config

import app.utils as ut

# url_eval = "http://127.0.0.1:5001"
# url_eval = Config.url_eval
@application.route('/books/all', methods=['GET'])
@application.route('/books', methods=['GET'])
@application.route('/books/', methods=['GET'])
@application.route('/', methods=['GET'])

def all_books():
    """
    Returns all book  in the database for Books
    service
    """
    books = ut.get_books()
    if len(books) == 0:
        abort(404)
    return make_response(jsonify({"books":books}),200)


@application.route('/books/<book_id>', methods=['GET'])
def book(book_id):
    """
    Returns a book  given a book id 
    :param book_id:
    :return: A Book
    """
    book = ut.get_book(book_id)
    if book is None:
        abort(404)
    return make_response(jsonify({"book": book.serialize()}),200)


@application.route('/books/add', methods=['POST'])
@application.route('/books', methods=['POST'])
def create_book():
    """ 
    Create a book object.
    :param book_id:
    :param request.json: a dictionnary containing fields
    'name' and 'year.

    :return: if success the created Book object
    """
    requested_fields = {'name', 'year'}
    included_fields = set(request.json.keys())
    if not request.json or not ut.test_intersection(requested_fields,included_fields):
        abort(400)
    book_name = request.json['name']
    book_year = request.json['year']

    book = ut.add_book(book_name, book_year)
    return make_response(jsonify({"book": book.serialize()}),201)


@application.route('/books/update/<book_id>', methods=['PUT'])
@application.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Updates a book based on its id.
    :param book_id:
    :param request.json: a dictionnary containing fields
    'name' and 'year.
    :return: if success the updated Book object
    """
    requested_fields = {'name', 'year'}
    included_fields = set(request.json.keys())

    book = ut.get_book(book_id)
    if book is None:
        abort(404)

    if not request.json:
        abort(400)

    if not ut.test_intersection(requested_fields,included_fields):
        abort(400)

    book_name = request.json['name']
    book_year = request.json['year']

    included_fields = set(request.json.keys())
    book = ut.update_book_by_id(book_id,book_name,book_year)
    return make_response(jsonify(book.serialize()))

@application.route('/books/delete/<book_id>', methods=['DELETE'])
@application.route('/books/<book_id>', methods=['DELETE'])
def del_book(book_id):
    """
    Deletes a book based on its id. Then calls the Evaluations service
    to delete all the evaluations related to this book
    :param book_id:
    :return: 
    """
    book = ut.get_book(book_id)
    if book is None:
        abort(404)
    ut.delete_book_by_id(book_id)

    #TODO replace with amqp protocol?
    try:
        requests.delete("{}/evaluations/books/{}".format(Config.evaluations_url,book_id))
    except requests.exceptions.ConnectionError:
        return make_response(jsonify({"error":"The Evaluations service is unavailable."}), 503)

    return make_response(jsonify({"Deleted":True}),200)

@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@application.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

