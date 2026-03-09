import numpy as np


def fuse_emotions(text=None, audio=None, video=None):
    """
    Fuse emotions from multiple modalities using weighted averaging.
    
    Args:
        text: dict with emotion and confidence from text analysis
        audio: dict with emotion and confidence from audio analysis
        video: dict with emotion and confidence from video analysis
        
    Returns:
        dict with fused emotion and confidence
    """
    
    # Define weights for each modality
    # Adjust based on reliability
    weights = {
        "text": 0.40,    # Text is often most reliable
        "audio": 0.35,   # Audio provides vocal cues
        "video": 0.25    # Video/facial expressions have highest variance
    }
    
    scores = {}
    total_weight = 0
    
    # Accumulate weighted emotion scores
    if text and text.get("emotion"):
        e = text["emotion"].lower()
        conf = min(text.get("confidence", 0), 100) / 100  # Normalize to 0-1
        score = conf * weights["text"]
        scores[e] = scores.get(e, 0) + score
        total_weight += weights["text"]
    
    if audio and audio.get("emotion"):
        e = audio["emotion"].lower()
        conf = min(audio.get("confidence", 0), 100) / 100
        score = conf * weights["audio"]
        scores[e] = scores.get(e, 0) + score
        total_weight += weights["audio"]
    
    if video and video.get("emotion"):
        e = video["emotion"].lower()
        conf = min(video.get("confidence", 0), 100) / 100
        score = conf * weights["video"]
        scores[e] = scores.get(e, 0) + score
        total_weight += weights["video"]
    
    # Handle case where no emotions detected
    if not scores or total_weight == 0:
        return {"emotion": "neutral", "confidence": 0.0}
    
    # Normalize scores by total weight
    normalized_scores = {k: (v / total_weight) * 100 for k, v in scores.items()}
    
    # Get emotion with highest score
    final_emotion = max(normalized_scores, key=normalized_scores.get)
    final_confidence = normalized_scores[final_emotion]
    
    return {
        "emotion": final_emotion,
        "confidence": final_confidence,
        "modalities": {
            "text": text.get("confidence", 0) if text else 0,
            "audio": audio.get("confidence", 0) if audio else 0,
            "video": video.get("confidence", 0) if video else 0
        }
    }


def fuse_emotions_advanced(text=None, audio=None, video=None, user_history=None):
    """
    Advanced emotion fusion considering temporal consistency.
    
    Args:
        text: dict with emotion and confidence
        audio: dict with emotion and confidence
        video: dict with emotion and confidence
        user_history: list of previous emotions (for temporal consistency)
        
    Returns:
        dict with fused emotion and confidence
    """
    
    # Get basic fusion
    fused = fuse_emotions(text, audio, video)
    
    # If user history exists, consider temporal consistency
    if user_history and len(user_history) > 0:
        recent_emotions = user_history[-5:]  # Last 5 emotions
        
        # Calculate emotion stability
        current_emotion = fused["emotion"]
        consistency_count = sum(1 for e in recent_emotions if e == current_emotion)
        consistency_score = consistency_count / len(recent_emotions)
        
        # Boost confidence if emotion is consistent with recent history
        fused["confidence"] = (fused["confidence"] * 0.7) + (consistency_score * 30)
        fused["consistency_score"] = consistency_score
    
    return fused