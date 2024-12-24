from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, database, models, hashing
from typing import List
from repository import user


router = APIRouter(
    prefix = '/user',
    tags = ['Users']
)


@router.get('/', response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(database.get_db)):
    return user.get_all(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.get_one(db, id)


@router.post('/', response_model=schemas.BaseUser)
def create_user(request: schemas.BaseUser, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    return user.delete(db, id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schemas.UpdateUser, db: Session = Depends(database.get_db)):
    return user.update(db, id, request)