from fastapi import FastAPI
from backend.database import engine
from backend import models
# from backend.auth import router as auth_router
from dotenv import load_dotenv
from backend.routers.chat import router as chat_router
from backend.routers import auth_routes, chat

load_dotenv()

app = FastAPI(title="AI Chatbot Backend")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "Backend running"}