from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(                     #Create Router and Register this in main.py
    tags=['Blogs']
)        

get_db = database.get_db

@router.get("/blog", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    
    for blog in blogs:
        print(blog.title, blog.user_id)
        
    return blogs


@router.post("/blog", status_code = status.HTTP_201_CREATED)       #This is to return the Status code back to the client
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body= request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/blog/{id}", status_code= status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
        
    return {'done'}


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_query.first()  # Check if the blog exists

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} not found"
        )

    # Perform the update
    blog_query.update(request.dict(), synchronize_session=False)
    db.commit()

    return {"detail": "Updated successfully"}

@router.get("/blog/{id}", status_code= 200, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} is not available!")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blow with id {id} is not available!"}
    return blog

