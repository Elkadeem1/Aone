from app.repositories import book_repo, user_repo
from app.schemas.schemas import CreateBook
from fastapi import HTTPException

def create_book(create_request: CreateBook):
    data = create_request.model_dump()
    data["status"] = "available"
    data["borrowed_by"] = None
    book_id = book_repo.insert_book(data)
    return {"id": str(book_id)}

def get_all_books():
    return [_book_helper(b) for b in book_repo.find_all_books()]

def get_book(book_id: str):
    try:
        book = book_repo.find_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return _book_helper(book)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID")

def borrow_book(book_id: str, user_id: str):
    if not user_repo.find_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")

    result = book_repo.update_book(
        book_id,
        {"status": "borrowed", "borrowed_by": user_id}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not available or not found")
    return {"message": "Book borrowed"}

def return_book(book_id: str):
    result = book_repo.update_book(
        book_id,
        {"status": "available", "borrowed_by": None}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not borrowed or not found")
    return {"message": "Book returned"}

def get_book_status_by_name(name: str):
    book = book_repo.find_book_by_name(name)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"name": book["name"], "status": book["status"]}

def _book_helper(book):
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "type": book["type"],
        "status": book["status"],
        "borrowed_by": book.get("borrowed_by")
    }
