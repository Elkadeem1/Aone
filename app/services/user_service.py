from app.repositories import user_repo
from app.schemas.schemas import CreateUser
from fastapi import HTTPException

def create_user(create_request: CreateUser):
    user_id = user_repo.insert_user(create_request.model_dump())
    return {"id": str(user_id)}

def get_all_users():
    return [{"id": str(u["_id"]), "name": u["name"], "age": u["age"]}
            for u in user_repo.find_all_users()]

def get_user(user_id: str):
    try:
        user = user_repo.find_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": str(user["_id"]), "name": user["name"], "age": user["age"]}
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")

def delete_user(user_id: str):
    try:
        result = user_repo.delete_user(user_id)
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted"}
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID")
