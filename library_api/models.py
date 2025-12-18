from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    name: str
    age: int

class CreateBook(BaseModel):
    name: str
    type: str
