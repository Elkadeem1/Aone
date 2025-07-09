from fastapi import APIRouter, HTTPException
from models import CreateUser
from database import Users
from bson import ObjectId

router = APIRouter()


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "age": user["age"]
    }


@router.post("/users")
def create_user(create_request: CreateUser):
    result = Users.insert_one(create_request.model_dump())
    return {"id": str(result.inserted_id)}


@router.get("/users")
def get_all_users():
    return [user_helper(u) for u in Users.find()]


@router.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        user = Users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user_helper(user)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        result = Users.delete_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
