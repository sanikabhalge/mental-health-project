# Maps raw model emotion labels → standardized labels used throughout the app

TEXT_EMOTION_MAP = {
    "angry":     "angry",
    "disgust":   "angry",       # DeepFace has disgust → map to angry
    "fear":      "fearful",
    "fearful":   "fearful",
    "happy":     "happy",
    "joy":       "happy",
    "sad":       "sad",
    "sadness":   "sad",
    "surprise":  "surprised",
    "surprised": "surprised",
    "neutral":   "neutral",
    "calm":      "calm",
}

# Legacy alias used by some modules
EMOTIONS_MAP = TEXT_EMOTION_MAP

EMOTIONS_DISPLAY = {
    "angry":     "Angry",
    "fearful":   "Fearful",
    "happy":     "Happy",
    "sad":       "Sad",
    "surprised": "Surprised",
    "neutral":   "Neutral",
    "calm":      "Calm",
}