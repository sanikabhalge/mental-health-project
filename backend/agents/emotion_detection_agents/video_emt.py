import cv2
import ffmpeg
import tempfile

from deepface import DeepFace

from utils.emotion_constants import TEXT_EMOTION_MAP
from agents.emotion_detection_agents.audio_emt import analyze_audio_emotion
from agents.emotion_detection_agents.fusion import fuse_emotions


def analyze_video_emotion(video_bytes):

    try:

        # ---------------- SAVE VIDEO ---------------- #

        with tempfile.NamedTemporaryFile(suffix=".webm") as temp_video:

            temp_video.write(video_bytes)
            temp_video.flush()

            video_path = temp_video.name

            # ---------------- EXTRACT AUDIO ---------------- #

            process = (
                ffmpeg
                .input(video_path)
                .output("pipe:1", format="webm")
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )

            audio_bytes, _ = process.communicate()

            audio_result = analyze_audio_emotion(audio_bytes)

            transcript = audio_result.get("transcript")
            audio_emotion = audio_result.get("emotion")
            audio_confidence = audio_result.get("confidence", 0.0)

            # ---------------- FACE EMOTION ---------------- #

            cap = cv2.VideoCapture(video_path)

            face_emotion = None
            face_confidence = 0.0

            frame_count = 0

            while cap.isOpened():

                ret, frame = cap.read()

                if not ret:
                    break

                frame_count += 1

                # sample every 20 frames
                if frame_count % 20 != 0:
                    continue

                try:

                    analysis = DeepFace.analyze(
                        frame,
                        actions=["emotion"],
                        enforce_detection=False
                    )

                    dominant = analysis[0]["dominant_emotion"]

                    face_confidence = float(analysis[0]["emotion"][dominant])

                    face_emotion = TEXT_EMOTION_MAP.get(dominant, "neutral")

                    break

                except Exception:
                    continue

            cap.release()

            # ---------------- FUSION ---------------- #

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
            "confidence": 0.5,
            "transcript": ""
        }