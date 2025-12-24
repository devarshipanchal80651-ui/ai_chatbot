from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.ai_service import get_ai_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    reply = get_ai_response(req.message)
    return {"reply": reply}