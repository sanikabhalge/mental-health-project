from fastapi import APIRouter, Depends
from schemas import ChatMessageCreate, ChatMessageResponse
from auth import get_current_user
from services.chat_service import process_chat_message

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(data: ChatMessageCreate, user=Depends(get_current_user)):
    """
    Process a chat message with multimodal emotion detection.

    Request body options:
    ┌─────────────────┬────────────────────────────────────────────────┐
    │ Field           │ Description                                    │
    ├─────────────────┼────────────────────────────────────────────────┤
    │ text            │ User's message text                            │
    │ audio_data      │ Base64 audio (webm/wav/mp3) → analyzed here    │
    │ video_data      │ Base64 image frame (jpg/png) → analyzed here   │
    │ audio_emotion   │ Pre-analyzed audio emotion (optional shortcut) │
    │ video_emotion   │ Pre-analyzed video emotion (optional shortcut) │
    │ mic_on          │ Whether mic is active (frontend flag)          │
    │ camera_on       │ Whether camera is active (frontend flag)       │
    │ session_id      │ Session identifier (optional)                  │
    └─────────────────┴────────────────────────────────────────────────┘

    Returns:
        reply            Empathetic AI response
        emotion_detected Fused dominant emotion
        confidence       Score 0–100
        mode             text | audio | video | multimodal | unknown
    """
    result = process_chat_message(data, user)
    return ChatMessageResponse(
        reply=result["reply"],
        emotion_detected=result.get("emotion_detected"),
        confidence=result.get("confidence"),
        mode=result.get("mode"),
    )