from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index():
    return {"data": "Blog List" }

@app.get('/blog')
def show(name: str, age: int, mobile: Optional[int] = None):

    print(type(name))
    if (name and age and mobile):
        return {"data":f'Name is {name} age is {age} and mobile is {mobile}'}
    return f'Hello {name}'

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(blog: Blog):             #Here blog is a Body from the Client which of the structure Blog
    return {"data": f"Blog Created with Name {blog.title}"}