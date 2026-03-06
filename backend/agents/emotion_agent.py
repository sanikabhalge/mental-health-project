from __future__ import annotations

import io
import tempfile
from functools import lru_cache
from typing import Literal, TypedDict


class EmotionDetectionResult(TypedDict):
    emotion: str
    confidence: float
    modality_used: str


Modality = Literal["text_only", "audio_only", "audio_video", "video_text"]


# Weights requested by the user
WEIGHTS = {"video": 0.4, "audio": 0.35, "text": 0.25}


def _detect_mode(*, text_message: str | None, audio_input: bytes | None, video_input: bytes | None) -> Modality:
    has_text = bool(text_message and text_message.strip())
    has_audio = audio_input is not None and len(audio_input) > 0
    has_video = video_input is not None and len(video_input) > 0

    if has_text and not has_audio and not has_video:
        return "text_only"
    if has_audio and not has_video and not has_text:
        return "audio_only"
    if has_audio and has_video:
        return "audio_video"
    if has_text and has_video and not has_audio:
        return "video_text"

    # If multiple are present but not covered above, prefer audio+video > video+text > text
    if has_audio and has_video:
        return "audio_video"
    if has_text and has_video:
        return "video_text"
    if has_audio:
        return "audio_only"
    return "text_only"


@lru_cache(maxsize=1)
def _text_pipeline():
    from transformers import pipeline

    # j-hartmann/emotion-english-distilroberta-base labels:
    # anger, disgust, fear, joy, neutral, sadness, surprise
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)


def detect_text_emotion(text: str) -> tuple[str, float]:
    text = (text or "").strip()
    if not text:
        return ("neutral", 0.0)

    try:
        pipe = _text_pipeline()
        out = pipe(text)
        # pipeline returns list[dict] or list[list[dict]] depending on version
        scores = out[0] if out and isinstance(out[0], list) else out
        best = max(scores, key=lambda d: float(d.get("score", 0.0)))
        label = str(best.get("label", "neutral")).lower()
        score = float(best.get("score", 0.0))
        return (label, score)
    except Exception:
        return ("neutral", 0.0)


@lru_cache(maxsize=1)
def _audio_model_bundle():
    import torch
    from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

    model_name = "superb/wav2vec2-base-superb-er"
    extractor = AutoFeatureExtractor.from_pretrained(model_name)
    model = AutoModelForAudioClassification.from_pretrained(model_name)
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return extractor, model, device


def _load_audio_waveform(audio_bytes: bytes) -> tuple["list[float] | any", int]:
    """
    Loads audio bytes into a mono waveform array + sample rate.
    Tries soundfile first (fast), then librosa.
    """
    try:
        import numpy as np
        import soundfile as sf

        data, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32", always_2d=False)
        if hasattr(data, "ndim") and data.ndim > 1:
            data = np.mean(data, axis=1)
        return data, int(sr)
    except Exception:
        try:
            import librosa

            y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None, mono=True)
            return y, int(sr)
        except Exception:
            return [], 16000


def _map_audio_label(label: str) -> str:
    # Common labels for superb-er: angry, happy, sad, neutral, etc.
    l = (label or "").strip().lower()
    if l == "happy":
        return "joy"
    if l == "sad":
        return "sadness"
    return l or "neutral"


def detect_audio_emotion(audio_bytes: bytes) -> tuple[str, float]:
    try:
        import numpy as np
        import torch

        extractor, model, device = _audio_model_bundle()
        waveform, sr = _load_audio_waveform(audio_bytes)
        if waveform is None or (hasattr(waveform, "__len__") and len(waveform) == 0):
            return ("neutral", 0.0)

        # Resample if needed
        target_sr = getattr(extractor, "sampling_rate", 16000) or 16000
        if sr != target_sr:
            try:
                import librosa

                waveform = librosa.resample(np.asarray(waveform), orig_sr=sr, target_sr=target_sr)
                sr = target_sr
            except Exception:
                pass

        inputs = extractor(waveform, sampling_rate=sr, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=-1)[0]
            idx = int(torch.argmax(probs).item())
            score = float(probs[idx].item())
            label = model.config.id2label.get(idx, "neutral")
        return (_map_audio_label(str(label)), score)
    except Exception:
        return ("neutral", 0.0)


def _map_video_emotion(label: str) -> str:
    l = (label or "").strip().lower()
    if l == "happy":
        return "joy"
    if l == "sad":
        return "sadness"
    return l or "neutral"


def _extract_frames_from_video_bytes(video_bytes: bytes, max_frames: int = 8):
    """
    Extract up to `max_frames` frames from video bytes.
    Falls back to treating bytes as an image.
    """
    try:
        import cv2
        import numpy as np

        # Try decode as image first
        img_arr = np.frombuffer(video_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if img is not None:
            return [img]

        # Otherwise write to temp file for VideoCapture
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as f:
            f.write(video_bytes)
            f.flush()
            cap = cv2.VideoCapture(f.name)
            frames = []
            count = 0
            stride = 1
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            if total > max_frames and total > 0:
                stride = max(1, total // max_frames)
            while cap.isOpened() and len(frames) < max_frames:
                ok, frame = cap.read()
                if not ok:
                    break
                if count % stride == 0:
                    frames.append(frame)
                count += 1
            cap.release()
            return frames
    except Exception:
        return []


def detect_video_emotion(video_bytes: bytes) -> tuple[str, float]:
    """
    Uses DeepFace to detect facial emotions from frames and aggregates predictions.
    If DeepFace isn't available, returns neutral with 0 confidence.
    """
    try:
        from deepface import DeepFace
        import numpy as np

        frames = _extract_frames_from_video_bytes(video_bytes, max_frames=8)
        if not frames:
            return ("neutral", 0.0)

        # Aggregate per-emotion scores across frames
        totals: dict[str, float] = {}
        n = 0
        for frame in frames:
            try:
                res = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                if isinstance(res, list):
                    res = res[0]
                emotion_scores = res.get("emotion") or {}
                if not isinstance(emotion_scores, dict):
                    continue
                for k, v in emotion_scores.items():
                    totals[_map_video_emotion(k)] = totals.get(_map_video_emotion(k), 0.0) + float(v)
                n += 1
            except Exception:
                continue

        if n == 0 or not totals:
            return ("neutral", 0.0)

        # DeepFace returns scores often in 0-100; normalize to 0-1
        best_emotion, best_score = max(totals.items(), key=lambda kv: kv[1])
        avg_score = (best_score / n) / 100.0
        avg_score = max(0.0, min(1.0, float(avg_score)))
        return (best_emotion, avg_score)
    except Exception:
        return ("neutral", 0.0)


def _fuse(
    *,
    text: tuple[str, float] | None,
    audio: tuple[str, float] | None,
    video: tuple[str, float] | None,
    modality_used: str,
) -> EmotionDetectionResult:
    scores: dict[str, float] = {}
    used_weight = 0.0

    if video:
        e, c = video
        scores[e] = scores.get(e, 0.0) + c * WEIGHTS["video"]
        used_weight += WEIGHTS["video"]
    if audio:
        e, c = audio
        scores[e] = scores.get(e, 0.0) + c * WEIGHTS["audio"]
        used_weight += WEIGHTS["audio"]
    if text:
        e, c = text
        scores[e] = scores.get(e, 0.0) + c * WEIGHTS["text"]
        used_weight += WEIGHTS["text"]

    if not scores or used_weight <= 0.0:
        return {"emotion": "neutral", "confidence": 0.0, "modality_used": modality_used}

    best_emotion, best_weighted = max(scores.items(), key=lambda kv: kv[1])
    confidence = best_weighted / used_weight
    confidence = max(0.0, min(1.0, float(confidence)))
    return {"emotion": best_emotion, "confidence": confidence, "modality_used": modality_used}


def initialize_models() -> None:
    """
    Preload models once at server start (performance requirement).
    """
    try:
        _text_pipeline()
    except Exception:
        pass
    try:
        _audio_model_bundle()
    except Exception:
        pass
    # DeepFace loads lazily on first call; we leave it lazy to avoid slow startup.


def detect_emotion(
    *,
    text_message: str | None = None,
    audio_input: bytes | None = None,
    video_input: bytes | None = None,
) -> EmotionDetectionResult:
    modality = _detect_mode(text_message=text_message, audio_input=audio_input, video_input=video_input)

    text_res: tuple[str, float] | None = None
    audio_res: tuple[str, float] | None = None
    video_res: tuple[str, float] | None = None

    if modality == "text_only":
        text_res = detect_text_emotion(text_message or "")
    elif modality == "audio_only":
        audio_res = detect_audio_emotion(audio_input or b"")
    elif modality == "audio_video":
        audio_res = detect_audio_emotion(audio_input or b"")
        video_res = detect_video_emotion(video_input or b"")
    elif modality == "video_text":
        video_res = detect_video_emotion(video_input or b"")
        text_res = detect_text_emotion(text_message or "")

    return _fuse(text=text_res, audio=audio_res, video=video_res, modality_used=modality)
