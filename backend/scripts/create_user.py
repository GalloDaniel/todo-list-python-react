import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal
from models import User
from jose import JWTError, jwt
from passlib.context import CryptContext

db = SessionLocal()

username = "admin"
password = "123456"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verifica se o usuário já existe
existing_user = db.query(User).filter_by(username=username).first()
if existing_user:
    db.delete(existing_user)
    db.commit()
    print("User already exists")

hashed = pwd_context.hash(password)
user = User(username=username, hashed_password=hashed)
db.add(user)
db.commit()
print("User created")
