
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pwd_ctx.hash(password)
    
    
    def verify(hashed_password, plane_password):
        return pwd_ctx.verify(plane_password, hashed_password)