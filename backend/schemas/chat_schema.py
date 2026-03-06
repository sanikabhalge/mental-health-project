from __future__ import annotations

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """
    Backward-compatible with the existing frontend payload:
    - older clients send `text`, `mic_on`, `camera_on`, `session_id`
    - newer clients can send `message` plus optional base64 audio/video
    """

    # Preferred
    message: str | None = Field(default=None, min_length=1)

    # Legacy field used by the current frontend
    text: str | None = None

    # Optional multimodal signals (base64-encoded bytes)
    audio_base64: str | None = None
    video_base64: str | None = None

    # Legacy flags (can still be sent by the frontend)
    mic_on: bool = False
    camera_on: bool = False

    # Kept for compatibility; history is stored per-user in DB
    session_id: str | None = None


class ChatMessageResponse(BaseModel):
    reply: str
    emotion: str
    confidence: float
    alert_level: str
