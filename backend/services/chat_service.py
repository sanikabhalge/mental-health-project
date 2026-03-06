from __future__ import annotations

from typing import Any, Literal, TypedDict

from sqlalchemy import desc
from sqlalchemy.orm import Session

from agents import chat_agent, emotion_agent
from agents.alert_agent import detect_suicide_risk
from models.chat_message import ChatMessage
from models.user import User


class ChatServiceResult(TypedDict):
    reply: str
    emotion: str
    confidence: float
    alert_level: str


CRISIS_SUPPORT_MESSAGE = (
    "I’m really sorry you’re feeling this way, and I’m glad you told me. "
    "If you’re in immediate danger or feel like you might harm yourself, please call your local emergency number right now. "
    "If you can, reach out to a trusted person near you and stay with them while you get support. "
    "You don’t have to go through this alone—would you like to tell me where you are and whether you’re safe right now?"
)


def _load_last_10_messages(db: Session, user_id: int) -> list[dict[str, str]]:
    rows: list[ChatMessage] = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(desc(ChatMessage.created_at), desc(ChatMessage.id))
        .limit(10)
        .all()
    )
    # DB fetch is newest-first; reverse to chronological for prompting
    rows.reverse()
    return [{"role": r.role, "content": r.content} for r in rows]


def _save_message(db: Session, *, user_id: int, role: Literal["user", "assistant"], content: str) -> None:
    db.add(ChatMessage(user_id=user_id, role=role, content=content))


def handle_chat_message(
    user: User,
    message: str,
    db: Session,
    audio: bytes | None = None,
    video: bytes | None = None,
) -> ChatServiceResult:
    """
    Orchestrates the agent flow:
    1) Load last 10 messages
    2) Detect emotion (text/audio/video)
    3) Run crisis detection (alert_agent + alert_service side effects)
    4) If HIGH risk: return crisis response (no chat_agent call)
    5) Otherwise: generate therapy response (Gemini)
    6) Save user + assistant messages
    """

    history = _load_last_10_messages(db, user.id)

    emotion_payload = emotion_agent.detect_emotion(
        text_message=message,
        audio_input=audio,
        video_input=video,
    )

    alert_level = "low"
    try:
        high_risk = bool(detect_suicide_risk(message, user))
    except Exception:
        # If the crisis detector fails, we keep the system running but do not block chat.
        high_risk = False

    if high_risk:
        alert_level = "high"
        reply = CRISIS_SUPPORT_MESSAGE
        _save_message(db, user_id=user.id, role="user", content=message)
        _save_message(db, user_id=user.id, role="assistant", content=reply)
        db.commit()
        return {
            "reply": reply,
            "emotion": emotion_payload["emotion"],
            "confidence": float(emotion_payload["confidence"]),
            "alert_level": alert_level,
        }

    user_profile = {
        "name": getattr(user, "name_for_profile", None) or user.username,
        "age": user.age or 0,
        "gender": user.gender or "unspecified",
    }

    reply = chat_agent.generate_therapy_reply(
        user_message=message,
        user_profile=user_profile,
        conversation_history=history,
        detected_emotion=emotion_payload["emotion"],
    )

    _save_message(db, user_id=user.id, role="user", content=message)
    _save_message(db, user_id=user.id, role="assistant", content=reply)
    db.commit()

    return {
        "reply": reply,
        "emotion": emotion_payload["emotion"],
        "confidence": float(emotion_payload["confidence"]),
        "alert_level": alert_level,
    }
