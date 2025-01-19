from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(                     #Create Router and Register this in main.py
    prefix= '/blog',                    # By having this all the endpoint will be prefixed with /blog so no need add again and again for all endpoints
    tags=['Blogs']
)        

get_db = database.get_db

@router.get("/", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post("/", status_code = status.HTTP_201_CREATED)       #This is to return the Status code back to the client
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.get("/{id}", status_code= 200, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    return blog.show(id, response, db)

