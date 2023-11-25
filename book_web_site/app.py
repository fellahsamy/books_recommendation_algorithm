from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'books.db')
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__= "books"
    isbn = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    year = db.Column(db.Integer())
    publisher = db.Column(db.String())
    image_m = db.Column(db.String())
    image_l = db.Column(db.String())
    mean_rating = db.Column(db.Float())
    count_rating = db.Column(db.Integer())
    reco_1 = db.Column(db.String())
    reco_2 = db.Column(db.String())
    reco_3 = db.Column(db.String())
    reco_4 = db.Column(db.String())
    reco_5 = db.Column(db.String())
    reco_6 = db.Column(db.String())
    reco_7 = db.Column(db.String())
    reco_8 = db.Column(db.String())
    reco_9 = db.Column(db.String())
    reco_10 = db.Column(db.String())

cnn = sqlite3.connect('books.db')

def rating_to_stars(mean_rating):
    num_stars = int(round(mean_rating ))
    return "★" * num_stars + "☆" * (10 - num_stars)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory("static",path)

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page)
    return render_template('index.html', books=books)

@app.route('/book/<isbn>')
def book_detail(isbn):
    # Search for the book by ISBN
    book = Book.query.filter_by(isbn=isbn).first()
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page)
    if book:
        reco_isbns = [getattr(book, f'reco_{i}') for i in range(2, 11) if getattr(book, f'reco_{i}')]
        recommended_books = Book.query.filter(Book.isbn.in_(reco_isbns)).all()
        mean_rating_stars = rating_to_stars(book.mean_rating)
        return render_template('index.html', books=books, book=book, recommended_books=recommended_books, mean_rating_stars=mean_rating_stars)
    else:
        return "Book not found", 404

if __name__ == '__main__':
    app.run()
