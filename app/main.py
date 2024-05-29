import uvicorn
from fastapi import FastAPI, Cookie, Response
from fastapi.responses import JSONResponse, HTMLResponse
import uuid

from datetime import datetime
from random import randrange
from models.models import User, Feedback, UserCreate, Product
from db import sample_products

app = FastAPI(title='MyFukingApp')

users = {'Kenny': {'password': 'qwerty', 'token': None},
         'Abrams': {'password': 'ytrewq', 'token': None}}


@app.post("/login/")
async def login(usr: User, resp: Response):
    if usr.username in users:
        if usr.password == users[usr.username]['password']:
            users[usr.username]['token'] = str(hash(usr.password)).replace('-','')
            resp.set_cookie(key='session_token', value=users[usr.username]['token'])
            return {'result': f'autorization success, token:{users[usr.username]['token']}'}    
        return {'result': f'Password is wrong'}
    
    return {'result': f'User {usr.username} not found'}


@app.get('/user')
async def user(token_id: str, resp: Response):
    for name,v in users.items():
        # print(token_id,[_ for _ in v.values()])
        if str(token_id) in [_ for _ in v.values()]:
            return name,v
    return {'result': 'Have not permissions'}



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



# @app.get('/')
# def read_root():
#     return {"message":"hello, World!"}


# @app.get("/custom")
# def read_custom_message():
#     return {"message": "This is a custom message!"}




if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8066,
        reload=True,
        workers=3
        )
