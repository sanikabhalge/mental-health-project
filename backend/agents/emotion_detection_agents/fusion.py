def fuse_emotions(text=None, audio=None, video=None):

    weights = {
        "text": 0.4,
        "audio": 0.35,
        "video": 0.25
    }

    scores = {}

    if text:
        e = text["emotion"]
        scores[e] = scores.get(e, 0) + text["confidence"] * weights["text"]

    if audio:
        e = audio["emotion"]
        scores[e] = scores.get(e, 0) + audio["confidence"] * weights["audio"]

    if video:
        e = video["emotion"]
        scores[e] = scores.get(e, 0) + video["confidence"] * weights["video"]

    if not scores:
        return {"emotion": "neutral", "confidence": 0}

    final_emotion = max(scores, key=scores.get)

    return {
        "emotion": final_emotion,
        "confidence": scores[final_emotion]
    }