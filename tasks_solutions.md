# 2.2
### Задание по программированию повышенной сложности:
Ваша задача состоит в том, чтобы расширить существующее приложение FastAPI, добавив новую конечную точку POST, которая принимает данные JSON, представляющие пользователя, и возвращает те же данные с дополнительным полем, указывающим, является ли пользователь взрослым или нет.

1. Определите Pydantic модель с именем "Пользователь" ("User") со следующими полями:

   - `name` (str)

   - `age` (int)

2. Создайте новый маршрут `/user`, который принимает запросы POST и принимает полезную нагрузку JSON, содержащую пользовательские данные, соответствующие модели `User`.

3. Реализуйте функцию для проверки того, является ли пользователь взрослым (возраст >= 18) или несовершеннолетним (возраст < 18).

4. Верните пользовательские данные вместе с дополнительным полем `is_adult` в ответе JSON, указывающим, является ли пользователь взрослым (True) или несовершеннолетним (False).

Пример:
Запрос в формате JSON:

{
    "name": "John Doe",
    "age": 25
}
Ответ в формате JSON:

{
    "name": "John Doe",
    "age": 25,
    "is_adult": true
}


# Solutions

### 1
```python
@app.post("/user")
async def show_user(usr: User_age):
    return {"name": usr.name,
            "age": usr.age,
            "is_adult": usr.age>=18}
```
### 2
```python
@app.post("/{User}")
def run(user: User):
    result = dict(user)
    result["is_adult"] = user.age > 17
    return result
```
### 3
```python
@app.post("/{User}")
def run(user: User):

    result = dict(user)
    result["is_adult"] = user.age > 17
    return result
```
### 4
```python
@app.post("/user")
async def add_user(user: User):
    is_adult = True if user.age >= 18 else False
    return {**user.model_dump(), "is_adult": is_adult}

```
### 5
```python
@app.post("/user")
async def return_Age(user: User):
    is_adult = True if user.age >= 18 else False
    return {'name':user.name,'age':user.age,'is_adult':is_adult}

```
***
# 2.3

### Задание по программированию:
Расширьте существующее приложение FastAPI, создав конечную точку POST, которая позволяет пользователям отправлять отзывы. Конечная точка должна принимать данные JSON, содержащие имя пользователя и сообщение обратной связи.

1. Определите Pydantic модель с именем "Feedback" (обратная связь) со следующими полями:
   - `name` (str)
   - `message` (str)

2. Создайте новый маршрут публикации "/feedback", который принимает данные JSON в соответствии с моделью `Feedback`.

3. Реализуйте функцию для обработки входящих данных обратной связи и ответа сообщением об успешном завершении.

4. Сохраните данные обратной связи в списке или хранилище данных, чтобы отслеживать все полученные отзывы.

Пример:
Запрос JSON:

{
    "name": "Alice",
    "message": "Great course! I'm learning a lot."
}
Ответ JSON:

{
    "message": "Feedback received. Thank you, Alice!"
}
Пожалуйста, протестируйте свою реализацию с помощью таких инструментов, как "curl", Postman или любой другой клиент API, чтобы отправить отзыв и проверить ответ

### Solutions
## 1 C записью в json
```python
from fastapi import FastAPI
from models import Feedback
import json
from pathlib import Path


app = FastAPI()

def save_json(file: str, to_json: dict) -> None:
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(to_json, f, indent=4, ensure_ascii=False, separators=(',', ': '))

def load_json(file_name: str) -> dict:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"user_msg":[]}

Path('data.json').touch()
data = load_json("data.json")

@app.post("/feedback")
async def user_feedback(msg: Feedback):
    data["user_msg"].append({"name": msg.name, "message": msg.message})
    save_json("data.json", data)
    return {"message": f"Feedback received. Thank you, {msg.name}!"}
```

### 2 С сохранением в db
```python
from database import connection_on_db, add_query


@app.post('/feedback')
async def create_feedback(feedback: Feedback):
    sql_query = '''
        INSERT INTO feedbacks (name, message)
        VALUES (? , ?);
    '''
    add_query(
        cursor=connection_on_db(),
        sql=sql_query,
        params=(feedback.name, feedback.message)
    )

    answear = {
        "message": f"Feedback received. Thank you, {feedback.name}!"
    }
    return JSONResponse(
        content=answear,
        status_code=201
    )


@app.get("/feedback")
async def get_feedbacks():
    sql_query = 'SELECT * FROM feedbacks;'
    data = add_query(cursor=connection_on_db(), sql=sql_query)
    return JSONResponse(content=data.fetchall(), status_code=200)
```

### 3 My

```python
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

```