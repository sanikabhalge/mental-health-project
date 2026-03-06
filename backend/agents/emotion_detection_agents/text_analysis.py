from transformers import pipeline
from utils.emotion_constants import TEXT_EMOTION_MAP

text_emotion_analyzer = pipeline(
    "sentiment-analysis",
    model="j-hartmann/emotion-english-distilroberta-base"
)

def text_emotion(text: str):

    if not text.strip():
        return {"emotion": "neutral", "confidence": 100}

    results = text_emotion_analyzer(text)

    top = results[0]
    label = top["label"].lower()
    score = float(top["score"] * 100)

    mapped = TEXT_EMOTION_MAP.get(label, label)

    return {
        "emotion": mapped,
        "confidence": score
    }