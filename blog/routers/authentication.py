
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags= ["Authentication"]
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Invalid Credentials! User with Username {request.username} not found"
        )
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Invalid Credentials! User with Password {request.password} not found"
        )
    
    # Generate JWT TOken and return
    return user