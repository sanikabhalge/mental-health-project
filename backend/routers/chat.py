from fastapi import APIRouter, Depends, UploadFile, File
from schemas import ChatMessageCreate, ChatMessageResponse
from auth import get_current_user

from services.chat_service import process_chat_message

router = APIRouter(prefix="/api/chat", tags=["Chat"])


# ---------------- TEXT CHAT ---------------- #

@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    data: ChatMessageCreate,
    user=Depends(get_current_user)
):

    result = await process_chat_message(data=data, user=user)

    return ChatMessageResponse(
        reply=result["reply"],
        emotion=result.get("emotion"),
        transcript=result.get("transcript"),
    )


# ---------------- AUDIO CHAT ---------------- #

@router.post("/audio", response_model=ChatMessageResponse)
async def send_audio(
    audio: UploadFile = File(...),
    user=Depends(get_current_user)
):

    audio_bytes = await audio.read()

    result = await process_chat_message(
        data=None,
        user=user,
        audio_bytes=audio_bytes
    )
    print("result",result)
    print("result reply",result["reply"])
    return ChatMessageResponse(
        reply=result["reply"],
        emotion=result.get("emotion"),
        transcript=result.get("transcript"),
    )


# ---------------- VIDEO CHAT ---------------- #

@router.post("/video", response_model=ChatMessageResponse)
async def send_video(
    video: UploadFile = File(...),
    user=Depends(get_current_user)
):

    video_bytes = await video.read()

    result = await process_chat_message(
        data=None,
        user=user,
        video_bytes=video_bytes
    )

    return ChatMessageResponse(
        reply=result["reply"],
        emotion=result.get("emotion"),
        transcript=result.get("transcript"),
    )