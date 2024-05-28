from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    age: str
    is_subscribed: bool

class Feedback(BaseModel):
    name: str
    message: str



class User(BaseModel):
    name: str
    age: int


# class User_id(BaseModel):
#     name: str
#     id: int
