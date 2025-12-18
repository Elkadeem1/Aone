from fastapi import FastAPI
from routers.users import router as user_router
from routers.books import router as book_router

app = FastAPI(title="Library API")

app.include_router(user_router)
app.include_router(book_router)