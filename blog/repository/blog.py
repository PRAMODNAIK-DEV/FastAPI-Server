from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body= request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db: Session):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
        
    return 'done'

def update(id: int, request: schemas.Blog, db):
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

def show(id: int, response, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} is not available!")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blow with id {id} is not available!"}
    return blog