from pydantic import BaseModel
from typing import Optional, Any


class EmotionResult(BaseModel):
    emotion: str = "neutral"
    confidence: float = 0.0


class ChatMessageCreate(BaseModel):
    text: Optional[str] = None
    audio_data: Optional[str] = None    # base64 encoded audio
    video_data: Optional[str] = None    # base64 encoded image frame
    audio_emotion: Optional[Any] = None # pre-analyzed (from /api/emotion/audio)
    video_emotion: Optional[Any] = None # pre-analyzed (from /api/emotion/video)
    mic_on: Optional[bool] = False
    camera_on: Optional[bool] = False
    session_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    reply: str
    emotion_detected: Optional[str] = None
    confidence: Optional[float] = None
    mode: Optional[str] = None  # "text" | "audio" | "video" | "multimodal"


class EmergencyContact(BaseModel):
    name: Optional[str] = None
    number: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    password: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[EmergencyContact] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse