from fastapi import FastAPI
from models import User, Gender, Role
from typing import List
from uuid import uuid4, UUID

app = FastAPI()

db: List[User] = [
    User(
        id=UUID('48420775-fd2f-4088-bab8-fb5078ec42ed'), 
        first_name='Maciek',
        last_name='Antosz',
        gender=Gender.male,
        roles=[Role.admin, Role.student]
    ),
    User(
        id=UUID('54186811-10a1-4824-a7e4-b9dfc4f46a3b'),
        first_name='Ahmed',
        last_name='Khalid',
        gender=Gender.female,
        roles=[Role.student]
    )
]

@app.get('/')
async def root():
    return {'Hello': 'Word'}

@app.get('/api/v1/users')
async def fetch_users():
    return db

@app.post('/api/v1/add_user')
async def register_user(user: User):
    db.append(user)
    return {'id': user.id}