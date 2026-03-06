from __future__ import annotations

from functools import lru_cache
from typing import Any

from google import genai
from google.genai import types

from config import settings


SYSTEM_PROMPT = """You are a supportive AI mental health companion who helps users reflect on their emotions.

Your goal is to create a safe space for the user to express feelings.

Rules:
- be empathetic
- use reflective listening
- ask open-ended questions
- avoid medical diagnosis
- avoid clinical terminology
- keep answers between 3 and 5 sentences
- never sound robotic
"""


@lru_cache(maxsize=1)
def _get_model() -> Any:
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def initialize_model() -> None:
    """
    Preload the Gemini model once at server start.
    """
    _get_model()


def _format_history(conversation_history: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for m in conversation_history[-10:]:
        role = (m.get("role") or "").strip().lower()
        content = (m.get("content") or "").strip()
        if not content:
            continue
        label = "User" if role == "user" else "Assistant"
        lines.append(f"{label}: {content}")
    return "\n".join(lines).strip()


def generate_therapy_reply(
    *,
    user_message: str,
    user_profile: dict[str, Any],
    conversation_history: list[dict[str, str]],
    detected_emotion: str,
) -> str:
    """
    Generates an empathetic therapy-style response using Gemini 1.5 Flash.
    Returns only the assistant message text.
    """

    profile_block = (
        "USER PROFILE\n"
        f"- name: {user_profile.get('name')}\n"
        f"- age: {user_profile.get('age')}\n"
        f"- gender: {user_profile.get('gender')}\n"
    )

    emotion_block = f"CURRENT EMOTION\n{detected_emotion}\n"

    history_block = "CONVERSATION HISTORY\n" + (_format_history(conversation_history) or "(no prior messages)") + "\n"

    latest_block = "LATEST USER MESSAGE\n" + user_message.strip() + "\n"

    prompt = (
        f"SYSTEM\n{SYSTEM_PROMPT}\n\n"
        f"{profile_block}\n"
        f"{emotion_block}\n"
        f"{history_block}\n"
        f"{latest_block}\n"
        "ASSISTANT RESPONSE (3-5 sentences):"
    )

    client = _get_model()
    if client is None:
        return (
            "I’m here with you. I can listen and support you, but the AI response system isn’t configured yet. "
            "Please ask the project owner to set `GEMINI_API_KEY` in `backend/.env`, and we can continue."
        )
    try:
        resp = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=types.Part.from_text(text=prompt),
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=350,
            ),
        )
        text = (getattr(resp, "text", None) or "").strip()
        return text or "I’m here with you. What’s been feeling the hardest lately?"
    except Exception:
        return "I’m here with you. What’s been feeling the hardest lately?"
