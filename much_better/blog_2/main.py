from fastapi import FastAPI, Depends, status, Response, HTTPException
import models, schemas, hashing
from database import engine, LocalSession
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, description='Create blog', tags=['Blogs'])
def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=2)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlogs], tags=['Blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blogs not found')
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blogs'])
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with this {id} is not available'}
    else:
        response.status_code = status.HTTP_201_CREATED
        return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'Blog Deleted'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update_blog(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)

    return {'details': 'Updated'}


@app.post('/user', response_model=schemas.ShowUser, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return {'details': 'User Deleted'}


@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Users'])
def update_user(id: int, request: schemas.UpdateUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    user.username = request.username
    user.email = request.email
    db.commit()
    db.refresh(user)

    return {'details': 'User Updated'}