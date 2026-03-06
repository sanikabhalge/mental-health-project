from __future__ import annotations

import base64

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from schemas.chat_schema import ChatMessageRequest, ChatMessageResponse
from services.chat_service import handle_chat_message

router = APIRouter(prefix="/chat", tags=["chat"])


def _decode_base64_maybe(data: str | None) -> bytes | None:
    if not data:
        return None
    try:
        # Accept both raw base64 and data URLs like: data:audio/wav;base64,AAAA
        if "," in data and data.strip().lower().startswith("data:"):
            data = data.split(",", 1)[1]
        return base64.b64decode(data, validate=False)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 payload for audio/video",
        )


@router.post("/message", response_model=ChatMessageResponse)
def send_message(
    data: ChatMessageRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChatMessageResponse:
    message = (data.message or data.text or "").strip()
    if not message:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Message is required")

    audio_bytes = _decode_base64_maybe(data.audio_base64)
    video_bytes = _decode_base64_maybe(data.video_base64)

    result = handle_chat_message(
        user=user,
        message=message,
        db=db,
        audio=audio_bytes,
        video=video_bytes,
    )

    return ChatMessageResponse(**result)
