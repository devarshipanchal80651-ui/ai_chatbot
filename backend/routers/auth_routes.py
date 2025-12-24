from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.auth import create_user, authenticate_user

router = APIRouter()

class Register(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(data: Register):
    db = SessionLocal()
    create_user(db, data.username, data.password)
    return {"msg": "Registered"}

@router.post("/login")
def login(data: Register):
    db = SessionLocal()
    if authenticate_user(db, data.username, data.password):
        return {"success": True}
    return {"success": False}