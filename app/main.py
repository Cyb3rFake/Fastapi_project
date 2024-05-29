import uvicorn
from fastapi import FastAPI, Cookie, Response


from datetime import datetime
from random import randrange
from models.models import User, Feedback, UserCreate, Product
from app.db import sample_products

app = FastAPI(title='MyFukingApp')
fake_db = [{'username': 'Anna', 'password': 'qwerty', 'session_token': None},
           {'username': 'Helga', 'password': 'qwerty', 'session_token': None}]


@app.get('/user')
def get_auth(session_token: str | None = Cookie(default=None)):
    return {"session_token":session_token}


@app.post('/login')
def auth(username:User,passwd:User,response:Response):
    db = fake_db[0]
    if username in db.keys() and db[username]==passwd:

        session_token= str(randrange(10000000,99999999))
        response.set_cookie(key = "session_token",value=session_token['session_token'])

        # return f'session_token: {response.headers.get('set-cookie').split(';')[0].split('=')[1]}'
        return {**session_token}



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



@app.get('/')
def read_root():
    return {"message":"hello, World!"}


@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!"}




if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8066,
        reload=True,
        workers=3
        )
