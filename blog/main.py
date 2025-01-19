from typing import List
from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
app = FastAPI()

# This line will crate all the tables in the database
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    except Exception as e:
        print("Error:", e)
        # Ensure the exception is re-raised
        raise
    finally:
        db.close()
        

@app.post("/blog", status_code = status.HTTP_201_CREATED, tags=['Blogs'])       #This is to return the Status code back to the client
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body= request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code= status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
        
    return {'done'}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
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


@app.get("/blog", response_model=List[schemas.ShowBlog], tags=['Blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", status_code= 200, response_model=schemas.ShowBlog, tags=['Blogs'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        # raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} is not available!")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blow with id {id} is not available!"}
    return blog



@app.post('/user', response_model=schemas.ShowUser, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name = request.name, email= request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {id} not found"
        )
    
    return user
