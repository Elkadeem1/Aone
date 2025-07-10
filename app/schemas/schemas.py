from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    age: int

class CreateBook(BaseModel):
    name: str
    type: str
