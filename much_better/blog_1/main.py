from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@app.get('/blog')
def index(limit: int = 20, published: bool = True, sort: Optional[bool] = None):
    if published:
        return {'data': {'blogs': f'till {limit} index; {sort}'}}
    else:
        return {'data': {'blogs': f'all indexes, {sort}'}}


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def show(id: int, limit: int = 10):
    return {
        f'data_{id}': {
            'limit': f'{limit}',
            'comment_1': 'not nice'
            }
        }


@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'Blog created, title: {request.title}'}


#if __name__ == "__main__":
#    uvicorn.run(app, host='127.0.0.1', port=80)