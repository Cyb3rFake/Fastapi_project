from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    name: str
    category: str 
    price: float


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool

class Feedback(BaseModel):
    name: str
    message: str



class User(BaseModel):
    username: str
    password: str
    session_token: None

# class User(BaseModel):
#     name: str
#     age: int


# class User_id(BaseModel):
#     name: str
#     id: int
