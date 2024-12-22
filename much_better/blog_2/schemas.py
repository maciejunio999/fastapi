from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    username: str
    email: str


class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List['ShowBlogs'] = []
    class Config:
        orm_mode = True


class ShowBlogs(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    creator: User
    class Config:
        orm_mode = True