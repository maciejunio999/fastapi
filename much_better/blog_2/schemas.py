from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlogs(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    class Config():
        orm_mode = True