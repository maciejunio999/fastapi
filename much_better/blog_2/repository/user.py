from sqlalchemy.orm import Session
import models, schemas, hashing
from fastapi import status, HTTPException, Response


def get_all(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is none")
    return users


def get_one(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


def create(request: schemas.BaseUser, db: Session):
    new_user = models.User(username=request.username, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete(db: Session, id: int):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'User Deleted'}


def update(db: Session, id: int, request: schemas.UpdateUser):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user.username = request.username
    user.email = request.email
    db.commit()
    db.refresh(user)

    return {'details': 'User Updated'}