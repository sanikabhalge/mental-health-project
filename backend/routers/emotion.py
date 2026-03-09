from fastapi import APIRouter, UploadFile, File, Request
from agents.emotion_detection_agents.audio_emt import analyze_audio
from agents.emotion_detection_agents.video_emt import analyze_face
import base64
from typing import Optional

router = APIRouter(prefix="/api/emotion", tags=["Emotion"])


def _decode_base64(data: str) -> Optional[bytes]:
    """Strip data-URI prefix and decode base64 to bytes."""
    try:
        if "," in data:
            data = data.split(",", 1)[1]
        return base64.b64decode(data)
    except Exception as e:
        print(f"[EmotionRouter] Base64 decode error: {e}")
        return None


@router.post("/audio")
async def audio_emotion(request: Request, file: UploadFile = File(None)):
    """
    Analyze emotion from audio.

    Accepts THREE formats:
      1. multipart/form-data  field name 'file'   (binary upload)
      2. application/json     field 'audio_data'  (base64 string)
      3. raw bytes body
    """
    try:
        audio_bytes = None
        content_type = request.headers.get("content-type", "")

        # Format 1: multipart file upload
        if file is not None:
            audio_bytes = await file.read()
            print(f"[EmotionRouter] Audio via multipart | size={len(audio_bytes)}")

        # Format 2: JSON base64
        elif "application/json" in content_type:
            body = await request.json()
            print(f"[EmotionRouter] JSON body keys: {list(body.keys())}")
            raw = (
                body.get("audio_data")
                or body.get("audio")
                or body.get("file")
                or body.get("data")
            )
            if raw:
                audio_bytes = _decode_base64(raw)
                print(f"[EmotionRouter] Audio via JSON base64 | size={len(audio_bytes) if audio_bytes else 0}")

        # Format 3: raw body
        else:
            audio_bytes = await request.body()
            if audio_bytes:
                print(f"[EmotionRouter] Audio via raw body | size={len(audio_bytes)}")

        if not audio_bytes:
            print("[EmotionRouter] No audio data received")
            return {"emotion": "neutral", "confidence": 0.0}

        result = analyze_audio(audio_bytes)
        print(f"[EmotionRouter] Audio result: {result}")
        return result

    except Exception as e:
        print(f"[EmotionRouter] Audio error: {e}")
        return {"emotion": "neutral", "confidence": 0.0}


@router.post("/video")
async def video_emotion(request: Request, file: UploadFile = File(None)):
    """
    Analyze emotion from image / video frame.

    Accepts THREE formats:
      1. multipart/form-data  field name 'file'   (binary upload)
      2. application/json     field 'video_data'  (base64 string)
      3. raw bytes body
    """
    try:
        video_bytes = None
        content_type = request.headers.get("content-type", "")

        # Format 1: multipart file upload
        if file is not None:
            video_bytes = await file.read()
            print(f"[EmotionRouter] Video via multipart | size={len(video_bytes)}")

        # Format 2: JSON base64
        elif "application/json" in content_type:
            body = await request.json()
            print(f"[EmotionRouter] JSON body keys: {list(body.keys())}")
            raw = (
                body.get("video_data")
                or body.get("image_data")
                or body.get("video")
                or body.get("image")
                or body.get("file")
                or body.get("data")
            )
            if raw:
                video_bytes = _decode_base64(raw)
                print(f"[EmotionRouter] Video via JSON base64 | size={len(video_bytes) if video_bytes else 0}")

        # Format 3: raw body
        else:
            video_bytes = await request.body()
            if video_bytes:
                print(f"[EmotionRouter] Video via raw body | size={len(video_bytes)}")

        if not video_bytes:
            print("[EmotionRouter] No video data received")
            return {"emotion": "neutral", "confidence": 0.0}

        result = analyze_face(video_bytes)
        print(f"[EmotionRouter] Video result: {result}")
        return result

    except Exception as e:
        print(f"[EmotionRouter] Video error: {e}")
        return {"emotion": "neutral", "confidence": 0.0}