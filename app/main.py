import uvicorn
from fastapi import FastAPI, Cookie, Response, Request ,Header, HTTPException, status, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uuid


from typing import Annotated
from datetime import datetime
from random import randrange
from models.models import User, Feedback, Product
from db import sample_products

app = FastAPI(title='MyFukingApp')

users = {'Kenny': {'password': 'qwerty', 'token': None},
         'Abrams': {'password': 'ytrewq', 'token': None}}




"""---------TASK 4.1----------"""

# security = HTTPBasic()
# USER_DATA = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]
# def get_user_from_db(username: str):
#     for user in USER_DATA:
#         if user.username == username:
#             return user
#     return None


# @app.get('/login')
# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     user = get_user_from_db(credentials.username)
#     if user is None or user.password!=credentials.password:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     return {"You got my secret, welcome"}


"""---------TASK 3.3 ---------"""

# @app.get("/headers")
# async def get_headers(request: Request):
#     user_agent = request.headers.get("user-agent")
#     accept_language = request.headers.get("accept-language")
    
#     # user_agent = request.headres.get("user-agent")
#     # accept_language = request.headres.get("accept-language")

#     if user_agent is None or accept_language is None:
#         raise HTTPException(status_code=400, detail="Missing required headers")

#     response_data = {
#         "User-Agent": user_agent,
#         "Accept-Language": accept_language
#     }
#     print(response_data)
#     return response_data




"""---------TASK 3.2 ---------"""
# @app.post("/login/")
# async def login(usr: User, resp: Response):
#     if usr.username in users:
#         if usr.password == users[usr.username]['password']:
#             users[usr.username]['token'] = str(hash(usr.password)).replace('-','')
#             resp.set_cookie(key='session_token', value=users[usr.username]['token'])
#             return {'result': f'autorization success, token:{users[usr.username]['token']}'}    
#         return {'result': f'Password is wrong'}
    
#     return {'result': f'User {usr.username} not found'}


# @app.get('/user')
# async def user(token_id: str, resp: Response):
#     for name,v in users.items():
#         # print(token_id,[_ for _ in v.values()])
#         if str(token_id) in [_ for _ in v.values()]:
#             return name,v
#     return {'result': 'Have not permissions'}

"""---------TASK 3.1---------"""

# @app.get('/products/search/')
# def search_product(keyword: str,category: str | None = None, limit:int | None = 10)-> list[Product]:
#     res = []
#     for product in sample_products:
#         if category and (category in product.values()):
#             if  keyword in product.values():
#                 res.append(product)
#                 return product
#             else:
#                 if limit:
#                     return [product for product in sample_products if product['category']==category][:limit]                
#                 else:
#                     return [product for product in sample_products if product['category']==category]
#         elif keyword in product.values():
#             return product


# @app.get('/product/{product_id}')
# def get_product(product_id: int)-> Product:
#     res = list(product for product in sample_products if product['product_id']==product_id)[0]
#     return res


"""---------TASK 3.1---------"""
# class UserCreate(BaseModel):
#     name: str
#     email: str
#     age: int
#     is_subscribed: bool

# @app.post('/create_user')
# def create_user(usr:UserCreate):
#     k = ('name',"email","age","is_subscribed")
#     v = (usr.name,usr.email,usr.age,usr.is_subscribed)
#     return dict(zip(k,v))
    

# @app.post('/feedback')
# def send_msg(usr: Feedback):
#     fake_db.append({'name':usr.name,'message':usr.message})
#     print(fake_db)
#     return {"message": f"Feedback received. Thank you, {usr.name}!"
#             }
"""---------TASK 2.2 ---------"""


# @app.get('/get_records')
# def get_records(user: str):
#     # print(fake_db)
#     messages = [i['message'] for i in fake_db if i['name']==user] 
#     print(messages)
#     return {'user': f'{user}',
#             'messages': messages
#             }



# @app.post("/user")
# def show_user(usr: User):
#     return {'name':usr.name,
#             'age':usr.age,
#             'is_adult': usr.age>=18
#             }

"""---------TASK 2.2 ---------"""
# EasyTask
# user_id = User_id(
#     name="John Doe",
#     id = 1
# )

# @app.get("/users_id")
# def get_users():
#     return {'name': user_id.name,'id': user_id.id}

# class User(BaseModel):
#     username: str
#     message: str
    

# @app.get('/test')
# def usr_msg(user: User):
#     return (f'Мы получили от юзера {user.username}\n\
#              такое сообщение: {user.message}\n\
#             в: {datetime.now()}')
"""---------TASK---------"""


@app.get('/')
def read_root():
    return {"message":"hello, World!"}


# @app.get("/custom")
# def read_custom_message():
#     return {"message": "This is a custom message!"}

"""---------TASK---------"""


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8066,
        reload=True,
        workers=3
        )
