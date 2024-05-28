from pydantic import BaseModel
from datetime import datetime
import uvicorn
from fastapi import FastAPI

from models.models import User, Feedback


app = FastAPI(title='MyFukingApp')

fake_db = []


@app.post('/feedback')
def send_msg(usr: Feedback):
    fake_db.append({'name':usr.name,'message':usr.message})
    print(fake_db)
    return {"message": f"Feedback received. Thank you, {usr.name}!"
            }



@app.get('/get_records')
def get_records(user: str):
    # print(fake_db)
    messages = [i['message'] for i in fake_db if i['name']==user] 
    print(messages)
    return {'user': f'{user}',
            'messages': messages
            }



@app.post("/user")
def show_user(usr: User):
    return {'name':usr.name,
            'age':usr.age,
            'is_adult': usr.age>=18
            }


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
