import base64
from typing import Optional

from agents.alert_agent import detect_suicide_risk
from agents.chat_agent import generate_chat_reply
from agents.emotion_detection_agents.text_analysis import text_emotion
from agents.emotion_detection_agents.audio_emt import analyze_audio
from agents.emotion_detection_agents.video_emt import analyze_face
from agents.emotion_detection_agents.fusion import fuse_emotions


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _decode_base64(data: str) -> Optional[bytes]:
    """Decode a base64 string (with or without data-URI prefix) to bytes."""
    try:
        if "," in data:                        # strip "data:audio/webm;base64,"
            data = data.split(",", 1)[1]
        return base64.b64decode(data)
    except Exception as e:
        print(f"[ChatService] Base64 decode error: {e}")
        return None


def _to_emotion_dict(obj) -> Optional[dict]:
    """Convert a Pydantic model or plain dict to a plain dict, or None if empty."""
    if obj is None:
        return None
    d = obj.dict() if hasattr(obj, "dict") else (obj if isinstance(obj, dict) else None)
    if not d or not d.get("emotion") or d.get("confidence", 0) == 0:
        return None
    return d


# ─────────────────────────────────────────────────────────────
# Main service
# ─────────────────────────────────────────────────────────────

def process_chat_message(data, user, user_emotion_history=None):
    """
    Multimodal emotion-aware chat handler.

    Priority for each modality:
      1. Raw base64 (audio_data / video_data) → decoded & analyzed here
      2. Pre-analyzed dict (audio_emotion / video_emotion) → used directly
      3. Not present → modality skipped

    Returns:
        dict: reply, emotion_detected, confidence, mode
    """

    text = (data.text or "").strip()

    # ── Crisis detection (text only) ──────────────────────────────────────
    if text:
        try:
            detect_suicide_risk(text, user)
        except Exception as e:
            print(f"[ChatService] Alert agent error: {e}")

    # ── Text emotion ──────────────────────────────────────────────────────
    text_emotion_result = None
    if text:
        try:
            text_emotion_result = text_emotion(text)
            print(f"[ChatService] Text emotion: {text_emotion_result}")
        except Exception as e:
            print(f"[ChatService] Text emotion error: {e}")

    # ── Audio emotion ─────────────────────────────────────────────────────
    audio_emotion_result = None

    if data.audio_data:
        audio_bytes = _decode_base64(data.audio_data)
        if audio_bytes:
            try:
                audio_emotion_result = analyze_audio(audio_bytes)
                print(f"[ChatService] Audio emotion (base64): {audio_emotion_result}")
            except Exception as e:
                print(f"[ChatService] Audio analysis error: {e}")
    elif data.audio_emotion:
        audio_emotion_result = _to_emotion_dict(data.audio_emotion)
        print(f"[ChatService] Audio emotion (pre-analyzed): {audio_emotion_result}")

    # ── Video emotion ─────────────────────────────────────────────────────
    video_emotion_result = None

    if data.video_data:
        video_bytes = _decode_base64(data.video_data)
        if video_bytes:
            try:
                video_emotion_result = analyze_face(video_bytes)
                print(f"[ChatService] Video emotion (base64): {video_emotion_result}")
            except Exception as e:
                print(f"[ChatService] Video analysis error: {e}")
    elif data.video_emotion:
        video_emotion_result = _to_emotion_dict(data.video_emotion)
        print(f"[ChatService] Video emotion (pre-analyzed): {video_emotion_result}")

    # ── Mode label ────────────────────────────────────────────────────────
    active = []
    if text_emotion_result:  active.append("text")
    if audio_emotion_result: active.append("audio")
    if video_emotion_result: active.append("video")

    mode = "unknown" if not active else ("multimodal" if len(active) > 1 else active[0])
    print(f"[ChatService] Mode: {mode} | Active: {active}")

    # ── Fuse emotions ─────────────────────────────────────────────────────
    if active:
        try:
            fused = fuse_emotions(
                text=text_emotion_result,
                audio=audio_emotion_result,
                video=video_emotion_result,
            )
            print(f"[ChatService] Fused: {fused}")
        except Exception as e:
            print(f"[ChatService] Fusion error: {e}")
            fused = {"emotion": "neutral", "confidence": 0.0}
    else:
        fused = {"emotion": "neutral", "confidence": 0.0}

    # ── Generate reply ────────────────────────────────────────────────────
    try:
        reply = generate_chat_reply(text=text or "...", current_emotion=fused, user=user)
    except Exception as e:
        print(f"[ChatService] Chat agent error: {e}")
        reply = "I'm here with you. Would you like to share a little more about how you're feeling?"

    return {
        "reply": reply,
        "emotion_detected": fused.get("emotion", "neutral"),
        "confidence": round(fused.get("confidence", 0.0), 2),
        "mode": mode,
    }