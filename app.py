from flask import Flask, request, jsonify
from database import app, db
from models import Book, Customer, Borrowing
from datetime import date
import bcrypt

@app.route('/')
def home():
    return "Welcome to the Library System API!"

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{ "id": book.id, "title": book.title, "author": book.author, "available": book.available } for book in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'], available=True)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({ "message": "Book added successfully!" }), 201

@app.route('/customers', methods=['POST'])
def register_customer():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_customer = Customer(name=data['name'], email=data['email'], password=hashed_password.decode('utf-8'))
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({ "message": "Customer registered successfully!" }), 201

@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    customer = Customer.query.get(data['customer_id'])
    book = Book.query.get(data['book_id'])
    
    if book and book.available:
        book.available = False
        new_borrowing = Borrowing(customer_id=customer.id, book_id=book.id, borrow_date=date.today())
        db.session.add(new_borrowing)
        db.session.commit()
        return jsonify({ "message": "Book borrowed successfully!" })
    else:
        return jsonify({ "error": "Book not available" }), 400

@app.route('/return', methods=['POST'])
def return_book():
    data = request.json
    borrowing = Borrowing.query.filter_by(customer_id=data['customer_id'], book_id=data['book_id'], return_date=None).first()
    
    if borrowing:
        borrowing.return_date = date.today()
        book = Book.query.get(borrowing.book_id)
        book.available = True
        db.session.commit()
        return jsonify({ "message": "Book returned successfully!" })
    else:
        return jsonify({ "error": "Borrowing record not found" }), 400

if __name__ == '__main__':
    app.run(debug=True)
