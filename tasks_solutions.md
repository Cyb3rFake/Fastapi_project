# Task 2.2
## Hard
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


### Solutions
#### 1
```python
@app.post("/user")
async def show_user(usr: User_age):
    return {"name": usr.name,
            "age": usr.age,
            "is_adult": usr.age>=18}
```
#### 2
```python
@app.post("/{User}")
def run(user: User):
    result = dict(user)
    result["is_adult"] = user.age > 17
    return result
```
#### 3
```python
@app.post("/{User}")
def run(user: User):

    result = dict(user)
    result["is_adult"] = user.age > 17
    return result
```
#### 4
```python
@app.post("/user")
async def add_user(user: User):
    is_adult = True if user.age >= 18 else False
    return {**user.model_dump(), "is_adult": is_adult}

```
#### 5
```python
@app.post("/user")
async def return_Age(user: User):
    is_adult = True if user.age >= 18 else False
    return {'name':user.name,'age':user.age,'is_adult':is_adult}

```
***
# Task 2.3
## Easy
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
#### 1 C записью в json
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

#### 2 С сохранением в db
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

#### 3 My

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

# Task 3.1 
## Easy
### Задание по программированию

Ваша задача - создать конечную точку FastAPI, которая принимает POST-запрос с данными о пользователе/юзере в теле запроса. Пользовательские данные должны включать следующие поля:

- `name` (str): Имя пользователя (обязательно).
- `email` (str): адрес электронной почты пользователя (обязателен и должен иметь допустимый формат электронной почты).
- `age` (int): возраст пользователя (необязательно, но должно быть положительным целым числом, если указано).
- `is_subscribed` (bool): Флажок, указывающий, подписан ли пользователь на новостную рассылку (необязательно).

 

1. Определите Pydantic модель с именем `UserCreate` для представления данных о пользователе. Применяйте соответствующие правила проверки, чтобы обеспечить правильность данных.

2. Создайте маршрут POST `/create_user`, который принимает данные JSON в соответствии с моделью `UserCreate`.

3. Реализуйте функцию для обработки входящих пользовательских данных и возврата ответа с полученной пользовательской информацией.

Пример:

Запрос JSON:

```json
{
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30,
    "is_subscribed": true
}
```
Ответ JSON:
```json
{
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30,
    "is_subscribed": true
}
```

##$ Solutions
#### 1 MY

```python

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool

@app.post('/create_user')
def create_user(usr:UserCreate):
    k = ('name',"email","age","is_subscribed")
    v = (usr.name,usr.email,usr.age,usr.is_subscribed)
    return dict(zip(k,v))
```

#### 2 с проверкой на отрицательный int
```python
#models
from pydantic import BaseModel, PositiveInt, Field, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=130)
    is_subscribed: bool = False

#routes
from fastapi import FastAPI
from models import UserCreate


app = FastAPI()
users: list[UserCreate] = []

@app.post("/create_user")
async def create_user(new_user: UserCreate):
    users.append(new_user)
    return new_user

@app.get("/showuser")
async def show_users():
    return {"users": users}


```

#### 3
```python

```
![](/solution_images/3_1.png)

# Task 3.1
## Hard
Задача программирования повышенной сложности
Ваша задача - создать приложение FastAPI, которое обрабатывает запросы, связанные с продуктами (товарами). Приложение должно иметь две конечные точки:

1. Конечная точка для получения информации о продукте:

   - Маршрут: `/product/{product_id}`

   - Метод: GET

   - Параметр пути:

     - `product_id`: идентификатор продукта (целое число)

   - Ответ: Возвращает объект JSON, содержащий информацию о продукте, основанную на предоставленном `product_id`.

2. Конечная точка для поиска товаров:

   - Маршрут: `/products/search`

   - Метод: GET

   - Параметры запроса:

     - `keyword` (строка, обязательна): ключевое слово для поиска товаров.

     - `category` (строка, необязательно): категория для фильтрации товаров.

     - `limit` (целое число, необязательно): максимальное количество товаров для возврата (по умолчанию 10, если не указано иное).

   - Ответ: Возвращает массив JSON, содержащий информацию о продукте, соответствующую критериям поиска.

3. Для примера можете использовать следующие данные с целью последующего направления ответа:
```python
sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}
```

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]
 

Пример:

Запрос GET на `/product/123` должен возвращать:
```json
{
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}
```
В ответ на GET-запрос на `/products/search?keyword=phone&category=Electronics&limit=5` должно вернуться:
```json
[
    {
        "product_id": 123,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 599.99
    },
    {
        "product_id": 789,
        "name": "Iphone",
        "category": "Electronics",
        "price": 1299.99
    },
]
```

Обратите внимание, что если маршруты будут одинаковыми (например, /products/{product_id} и /products/search), то у нас второй маршрут будет не рабочим, тк слово search FastAPI будет пытаться привести к int, то есть обработать первый маршрут, и выдаст ошибку). Маршруты обрабатываются в порядке объявления хендлеров). 
## Solutions 3.1
#### 1 My
```python
#models

class Product(BaseModel):
    product_id: int
    name: str
    category: str 
    price: float


#routes
@app.get('/products/search/')
def search_product(keyword: str,category: str | None = None, limit:int | None = 10)-> list[Product]:
    res = []
    for product in sample_products:
        if category and (category in product.values()):
            if  keyword in product.values():
                res.append(product)
                return product
            else:
                if limit:
                    return [product for product in sample_products if product['category']==category][:limit]                
                else:
                    return [product for product in sample_products if product['category']==category]
        elif keyword in product.values():
            return product


@app.get('/product/{product_id}')
def get_product(product_id: int)-> Product:
    res = list(product for product in sample_products if product['product_id']==product_id)[0]
    return res
```

# Task 3.2
Задача на программирование
Ваша задача - создать приложение FastAPI, которое реализует аутентификацию на основе файлов cookie. Выполните следующие действия:

1. Создайте простой маршрут входа в систему по адресу "/login", который принимает имя пользователя и пароль в качестве данных формы. Если учетные данные действительны, установите безопасный файл cookie только для HTTP с именем "session_token" с уникальным значением.

2. Реализуйте защищенный маршрут в "/user", который требует аутентификации с использованием файла cookie "session_token". Если файл cookie действителен и содержит правильные данные аутентификации, верните ответ в формате JSON с информацией профиля пользователя.

3. Если файл cookie "session_token" отсутствует или недействителен, маршрут "/user" должен возвращать ответ об ошибке с кодом состояния 401 (неавторизован) или сообщение {"message": "Unauthorized"}.

Пример:

POST-запрос в `/login` с данными формы:
```json
{
  "username": "user123",
  "password": "password123"
} 
```
Ответ должен содержать файл cookie "session_token".

GET-запрос к `/user` с помощью файла cookie "session_token":

session_token: "abc123xyz456"
Ответ должен возвращать информацию профиля пользователя.

GET-запрос к `/user` без файла cookie "session_token" или с недопустимым файлом cookie, например:

session_token: "invalid_token_value"
Ответ должен возвращать сообщение об ошибке с кодом состояния 401 или сообщение {"message": "Unauthorized"}.

Пожалуйста, протестируйте свою реализацию с помощью таких инструментов, как "curl", Postman или любой другой клиент API, чтобы проверить функциональность аутентификации на основе файлов cookie.