
from typing import List, Optional
from pydantic import BaseModel

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True
    

class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]
    
    class Config():
        orm_mode = True

    
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    # creator: Optional[ShowUser]     #Made this opttional if the user_id Column in Blog is Null in DB
    
    class Config():
        orm_mode = True
