from fastapi import APIRouter, Query
from app.services import book_service
from app.schemas.schemas import CreateBook

router = APIRouter()

@router.post("/books")
def create_book(create_request: CreateBook):
    return book_service.create_book(create_request)

@router.get("/books")
def get_all_books():
    return book_service.get_all_books()

@router.get("/books/{book_id}")
def get_book(book_id: str):
    return book_service.get_book(book_id)

@router.patch("/books/{book_id}/borrow")
def borrow_book(book_id: str, user_id: str):
    return book_service.borrow_book(book_id, user_id)

@router.patch("/books/{book_id}/return")
def return_book(book_id: str):
    return book_service.return_book(book_id)

@router.get("/books/status")
def get_book_status_by_name(name: str = Query(..., description="Book name to check status")):
    return book_service.get_book_status_by_name(name)
