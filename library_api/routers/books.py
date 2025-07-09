from fastapi import APIRouter, HTTPException
from models import CreateBook
from database import Books, Users
from bson import ObjectId
from fastapi import Query


router = APIRouter()


def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "type": book["type"],
        "status": book["status"],
        "borrowed_by": book.get("borrowed_by")
    }


@router.post("/books")
def create_book(create_request: CreateBook):
    book_data = create_request.dict()
    book_data["status"] = "available"
    book_data["borrowed_by"] = None
    result = Books.insert_one(book_data)
    return {"id": str(result.inserted_id)}


@router.get("/books")
def get_all_books():
    return [book_helper(b) for b in Books.find()]


@router.get("/books/{book_id}")
def get_book(book_id: str):
    try:
        book = Books.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book_helper(book)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID")


@router.patch("/books/{book_id}/borrow")
def borrow_book(book_id: str, user_id: str):
    if not Users.find_one({"_id": ObjectId(user_id)}):
        raise HTTPException(status_code=404, detail="User not found")

    result = Books.update_one(
        {"_id": ObjectId(book_id), "status": "available"},
        {"$set": {"status": "borrowed", "borrowed_by": user_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not available or not found")
    return {"message": "Book borrowed"}


@router.patch("/books/{book_id}/return")
def return_book(book_id: str):
    result = Books.update_one(
        {"_id": ObjectId(book_id), "status": "borrowed"},
        {"$set": {"status": "available", "borrowed_by": None}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not borrowed or not found")
    return {"message": "Book returned"}

#get book status
@router.get("/books/status")
def get_book_status_by_name(name: str = Query(..., description="Book name to check status")):
    book = Books.find_one({"name": name})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "name": book["name"],
        "status": book["status"]
    }