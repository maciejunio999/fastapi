from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
import schemas, database
from typing import List
from repository import blog


router = APIRouter(
    prefix = '/blog',
    tags = ['Blogs']
)


@router.get('/', response_model=List[schemas.ShowBlogs])
def get_all_blogs(db: Session = Depends(database.get_db)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, description='Create blog')
def create(request: schemas.BlogBase, db: Session = Depends(database.get_db)):
    return blog.create(db, request)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_blog(id: int, response: Response, db: Session = Depends(database.get_db)):
    return blog.get_one(db, id, response)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db)):
    return blog.delete(db, id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.BlogBase, db: Session = Depends(database.get_db)):
    return blog.update(db, id, request)