EMOTIONS_MAP = {
    0: 'neutral',
    1: 'calm',
    2: 'happy',
    3: 'sad',
    4: 'angry',
    5: 'fearful',
    6: 'disgust',
    7: 'surprised'
}

TEXT_EMOTION_MAP = {
    'anger': 'angry',
    'disgust': 'disgust',
    'fear': 'fearful',
    'joy': 'happy',
    'neutral': 'neutral',
    'sadness': 'sad',
    'surprise': 'surprised'
}

EMOTION_DIMENSIONS = {
    'neutral': {'valence': 0.0, 'arousal': 0.0},
    'calm': {'valence': 0.3, 'arousal': -0.5},
    'happy': {'valence': 0.8, 'arousal': 0.6},
    'sad': {'valence': -0.7, 'arousal': -0.6},
    'angry': {'valence': -0.8, 'arousal': 0.8},
    'fearful': {'valence': -0.9, 'arousal': 0.9},
    'disgust': {'valence': -0.6, 'arousal': 0.4},
    'surprised': {'valence': 0.0, 'arousal': 0.7}
}