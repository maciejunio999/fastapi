from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import schemas, database, models
from typing import List


router = APIRouter(
    prefix = '/blog',
    tags = ['Blogs']
)


@router.get('/', response_model=List[schemas.ShowBlogs])
def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blogs not found')
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED, description='Create blog')
def create(request: schemas.BlogBase, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_blog(id: int, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with this {id} is not available'}
    else:
        response.status_code = status.HTTP_201_CREATED
        return blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Blog Deleted'}


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.BlogBase, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)

    return {'details': 'Blog Updated'}