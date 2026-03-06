from fastapi import APIRouter, Depends
from schemas import ChatMessageCreate, ChatMessageResponse
from auth import get_current_user
from services.chat_service import process_chat_message

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(data: ChatMessageCreate, user=Depends(get_current_user)):
    
    reply = process_chat_message(data, user)

    return ChatMessageResponse(reply=reply)