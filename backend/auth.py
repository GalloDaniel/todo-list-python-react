from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User
from auth_token import create_access_token, verify_token
from database import SessionLocal
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
