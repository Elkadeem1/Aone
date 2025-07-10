from fastapi import APIRouter
from app.services import user_service
from app.schemas.schemas import CreateUser

router = APIRouter()

@router.post("/users")
def create_user(create_request: CreateUser):
    return user_service.create_user(create_request)

@router.get("/users")
def get_all_users():
    return user_service.get_all_users()

@router.get("/users/{user_id}")
def get_user(user_id: str):
    return user_service.get_user(user_id)

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    return user_service.delete_user(user_id)
