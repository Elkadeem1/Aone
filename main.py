from fastapi import FastAPI
from app.api import books, users

app = FastAPI(title="Library API")

app.include_router(users.router)
app.include_router(books.router)
