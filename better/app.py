from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdate
from typing import List
from uuid import UUID

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

@app.delete("/api/v1/delete_user")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"Deleted": "User"}
    raise HTTPException(
        status_code=404,
        detail=f"User not found for id: {user_id}"
    )

@app.put('/api/v1/update_user/{user_id}')
async def update_user(user_update: UserUpdate, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            return {"Updated": "User"}
    raise HTTPException(
        status_code=404,
        detail=f"User not found for id: {user_id}"
    )