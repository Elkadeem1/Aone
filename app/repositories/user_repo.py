from app.db.database import db
from bson import ObjectId

Users = db.users

def insert_user(data: dict):
    return Users.insert_one(data).inserted_id

def find_all_users():
    return list(Users.find())

def find_user_by_id(user_id: str):
    return Users.find_one({"_id": ObjectId(user_id)})

def delete_user(user_id: str):
    return Users.delete_one({"_id": ObjectId(user_id)})
