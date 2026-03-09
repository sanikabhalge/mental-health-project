import cv2
import numpy as np
import tempfile
import os
from deepface import DeepFace
from utils.emotion_constants import TEXT_EMOTION_MAP


def analyze_video_frame_deepface(image_data):
    """
    Analyze facial emotion from an image using DeepFace.

    Args:
        image_data: bytes | file path str | numpy array

    Returns:
        dict: { emotion: str, confidence: float }
    """
    temp_file = None
    try:
        # ── Convert input → OpenCV image ──────────────────────────────────
        if isinstance(image_data, bytes):
            arr   = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        elif isinstance(image_data, str):
            image = cv2.imread(image_data)
        elif isinstance(image_data, np.ndarray):
            image = image_data
        else:
            print("[Video] Unsupported image_data type")
            return {"emotion": "neutral", "confidence": 0}

        if image is None:
            print("[Video] Could not decode image")
            return {"emotion": "neutral", "confidence": 0}

        # ── Save to temp file (DeepFace requires a path) ──────────────────
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_file = tmp.name
        cv2.imwrite(temp_file, image)

        # ── Run DeepFace ──────────────────────────────────────────────────
        analysis = DeepFace.analyze(
            img_path=temp_file,
            actions=["emotion"],
            enforce_detection=False,    # don't crash if no face found
            detector_backend="opencv",  # fastest backend
            silent=True,
        )

        if not analysis:
            print("[Video] DeepFace returned empty result")
            return {"emotion": "neutral", "confidence": 0}

        result      = analysis[0]
        emotion_dict = result.get("emotion", {})
        dominant    = result.get("dominant_emotion", "neutral")
        confidence  = float(emotion_dict.get(dominant, 0))
        mapped      = TEXT_EMOTION_MAP.get(dominant.lower(), dominant.lower())

        print(f"[Video] → {dominant} ({confidence:.1f}%) | mapped={mapped}")
        return {"emotion": mapped, "confidence": round(confidence, 2)}

    except Exception as e:
        print(f"[Video] Error: {e}")
        return {"emotion": "neutral", "confidence": 0}
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass


def analyze_face(image_data):
    """Main entry point for facial emotion analysis."""
    return analyze_video_frame_deepface(image_data)


def detect_faces_and_emotions(image_data):
    """Detect all faces in an image and return emotion for each."""
    temp_file = None
    try:
        if isinstance(image_data, bytes):
            arr   = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        elif isinstance(image_data, str):
            image = cv2.imread(image_data)
        else:
            image = image_data

        if image is None:
            return []

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            temp_file = tmp.name
        cv2.imwrite(temp_file, image)

        results = DeepFace.analyze(
            img_path=temp_file,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv",
            silent=True,
        )

        return [
            {
                "emotion": TEXT_EMOTION_MAP.get(r.get("dominant_emotion", "neutral").lower(),
                                                r.get("dominant_emotion", "neutral").lower()),
                "confidence": round(float(r.get("emotion", {}).get(r.get("dominant_emotion", "neutral"), 0)), 2),
            }
            for r in results
        ]

    except Exception as e:
        print(f"[Video] detect_faces_and_emotions error: {e}")
        return []
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass