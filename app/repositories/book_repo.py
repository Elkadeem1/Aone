from app.db.database import db
from bson import ObjectId

Books = db.books

def insert_book(data: dict):
    return Books.insert_one(data).inserted_id

def find_all_books():
    return list(Books.find())

def find_book_by_id(book_id: str):
    return Books.find_one({"_id": ObjectId(book_id)})

def update_book(book_id: str, update_data: dict):
    return Books.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})

def find_book_by_name(name: str):
    return Books.find_one({"name": name})
