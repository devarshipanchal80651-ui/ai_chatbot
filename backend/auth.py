from passlib.context import CryptContext
from backend.models import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str):
    # safe_password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db, username, password):
    user = User(
        username=username,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return verify_password(password, user.password_hash)

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from backend.database import get_db
# from backend.models import User
# from backend.security import verify_password, create_token
# from passlib.context import CryptContext
#
# router = APIRouter()
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def hash_password(password: str):
#     return pwd_context.hash(password)
#
# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)
#
# def create_user(db: Session, username: str, password: str):
#     user = User(username=username, password=hash_password(password))
#     db.add(user)
#     db.commit()
#
# def authenticate_user(db: Session, username: str, password: str):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return True
#
# @router.post("/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#
#     if not user or not verify_password(password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#
#     token = create_token({"sub": user.username})
#
#     return {
#         "msg": "Login successful",
#         "access_token": token
#     }