import cv2
import ffmpeg
import tempfile
import os

from deepface import DeepFace

from utils.emotion_constants import TEXT_EMOTION_MAP
from agents.emotion_detection_agents.audio_emt import analyze_audio_emotion
from agents.emotion_detection_agents.fusion import fuse_emotions


def analyze_video_emotion(video_bytes):

    video_path = None
    wav_path = None

    try:

        # -------- SAVE VIDEO (Windows safe) -------- #

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
        temp.write(video_bytes)
        temp.close()

        video_path = temp.name

        # sanity check
        if os.path.getsize(video_path) < 5000:
            print("video too small → corrupted")
            return {
                "emotion": "neutral",
                "confidence": 0.0,
                "transcript": ""
            }

        # -------- EXTRACT AUDIO → WAV -------- #

        wav_path = video_path.replace(".webm", ".wav")

        (
            ffmpeg
            .input(video_path)
            .output(wav_path, ac=1, ar=16000)
            .run(overwrite_output=True, quiet=True)
        )

        audio_bytes = b""
        if os.path.exists(wav_path):
            with open(wav_path, "rb") as f:
                audio_bytes = f.read()

        audio_emotion = None
        audio_confidence = 0.0
        transcript = ""

        if audio_bytes:
            audio_result = analyze_audio_emotion(audio_bytes)
            transcript = audio_result.get("transcript", "")
            audio_emotion = audio_result.get("emotion")
            audio_confidence = audio_result.get("confidence", 0.0)

        # -------- FACE EMOTION -------- #

        cap = cv2.VideoCapture(video_path)

        face_emotion = None
        face_confidence = 0.0
        frame_count = 0

        while cap.isOpened():

            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            if frame_count % 15 != 0:
                continue

            try:

                analysis = DeepFace.analyze(
                    frame,
                    actions=["emotion"],
                    enforce_detection=False
                )

                dominant = analysis[0]["dominant_emotion"]

                face_confidence = float(
                    analysis[0]["emotion"][dominant]
                )

                face_emotion = TEXT_EMOTION_MAP.get(
                    dominant,
                    "neutral"
                )

                break

            except Exception:
                continue

        cap.release()

        # -------- FUSION -------- #

        emotion_detected, confidence = fuse_emotions(
            audio_emotion,
            face_emotion,
            audio_confidence,
            face_confidence
        )

        result = {
            "emotion": emotion_detected,
            "confidence": confidence,
            "transcript": transcript
        }

        print("video emotion detected:", result)

        return result

    except Exception as e:

        print("video emotion error:", e)

        return {
            "emotion": "neutral",
            "confidence": 0.0,
            "transcript": ""
        }

    finally:

        if video_path and os.path.exists(video_path):
            os.remove(video_path)

        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)