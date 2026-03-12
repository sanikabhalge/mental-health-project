import numpy as np
import librosa
import tempfile
import os
import whisper
import tensorflow as tf
from config import settings
from utils.emotion_constants import EMOTIONS_MAP


# ---------------- LOAD MODELS ---------------- #



emotion_model = tf.keras.models.load_model(settings.MODEL_PATH)
whisper_model = whisper.load_model("base")


# ---------------- FEATURE EXTRACTION ---------------- #

def extract_features(audio_data, sr, n_mfcc=40, n_mels=128):

    if isinstance(audio_data, np.ndarray) and audio_data.ndim > 1:
        audio_data = audio_data.flatten()

    if len(audio_data) < sr * 0.1:
        return None

    result = np.array([])

    # MFCC
    mfccs = np.mean(
        librosa.feature.mfcc(
            y=audio_data,
            sr=sr,
            n_mfcc=n_mfcc
        ).T,
        axis=0
    )

    result = np.hstack((result, mfccs))

    # CHROMA
    try:
        stft = np.abs(librosa.stft(audio_data))
        chroma = np.mean(
            librosa.feature.chroma_stft(
                S=stft,
                sr=sr
            ).T,
            axis=0
        )

        result = np.hstack((result, chroma))

    except Exception:
        result = np.hstack((result, np.zeros(12)))

    # MEL SPECTROGRAM
    mel = np.mean(
        librosa.feature.melspectrogram(
            y=audio_data,
            sr=sr,
            n_mels=n_mels
        ).T,
        axis=0
    )

    result = np.hstack((result, mel))

    # Ensure feature length = 180
    expected_feature_length = 180

    if result.shape[0] < expected_feature_length:

        result = np.pad(
            result,
            (0, expected_feature_length - result.shape[0]),
            "constant"
        )

    elif result.shape[0] > expected_feature_length:

        result = result[:expected_feature_length]

    return result
def analyze_audio_emotion(audio_bytes):

    try:

        # -------- SAVE TEMP FILE -------- #

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:

            temp.write(audio_bytes)
            audio_path = temp.name

        # -------- TRANSCRIPTION -------- #

        transcript = ""

        try:

            whisper_result = whisper_model.transcribe(
                                audio_path,
                                language="en",
                                task="transcribe",
                                fp16=False
                            )

            transcript = whisper_result.get("text", "").strip()
            # remove non-english transcripts
            if not transcript.isascii():
                transcript = ""
        except Exception as e:

            print("whisper error:", e)

        # -------- LOAD AUDIO -------- #

        audio_data, sr = librosa.load(audio_path, sr=22050)

        # -------- FEATURE EXTRACTION -------- #

        features = extract_features(audio_data, sr)

        if features is None:

            return {
                "emotion": "neutral",
                "confidence": 0.0,
                "transcript": transcript
            }

        features = features.reshape(1, -1, 1)

        # -------- MODEL PREDICTION -------- #

        prediction = emotion_model.predict(features, verbose=0)

        idx = np.argmax(prediction)

        confidence = float(np.max(prediction) * 100)

        emotion_label = EMOTIONS_MAP.get(idx, "neutral")

        result = {
            "emotion": emotion_label,
            "confidence": confidence,
            "transcript": transcript
        }

        print("audio emotion detected:", result)

        os.remove(audio_path)

        return result

    except Exception as e:

        print("audio emotion error:", e)

        return {
            "emotion": "neutral",
            "confidence": 0.0,
            "transcript": ""
        }