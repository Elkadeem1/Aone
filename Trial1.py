from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.user_db
collection = db.users

app = FastAPI()

# Helper function to convert MongoDB documents
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "age": user["age"]
    }

# Pydantic models
class User(BaseModel):
    name: str = Field(default="OLD")
    age: int = Field(default=20)
    id: str = Field(default="007")

class UserDB(User):
    id: str

# POST - Create User
@app.post("/create", response_model=UserDB)
def create_user(user: User):
    result = collection.insert_one(user.dict())
    new_user = collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

# GET - Read All Users
@app.get("/get_all_users", response_model=List[UserDB])
def get_all_users():
    users = []
    for user in collection.find():
        users.append(user_helper(user))
    return users

# GET - Read Single User
@app.get("/get_user/{user_id}", response_model=UserDB)
def get_user(user_id: str):
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

# PUT - Update User
@app.put("/update_user/{user_id}", response_model=UserDB)
def update_user(user_id: str, updated_user: User):
    try:
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_user.dict()}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user = collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(user)

# DELETE - Delete User
@app.delete("/delete/{user_id}")
def delete_user(user_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}