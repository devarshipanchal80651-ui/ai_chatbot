from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db, SessionLocal
from backend.models import User
from backend.auth import hash_password, verify_password, create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code = 400, detail="User already exists")

    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"msg": "Registered"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Invalid credentials")

    # token = create_token({"sub": user.username})
    # return {"access_token": token}

    return {"message": "Logged in successfully"}
