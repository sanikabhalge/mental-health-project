# import librosa
# import numpy as np
# import tensorflow as tf
# from utils.emotion_constants import EMOTIONS_MAP
# from config import settings


# ver_model = tf.keras.models.load_model(settings.MODEL_PATH)


# def extract_features(audio, sr=22050, n_mfcc=40):

#     mfcc = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc).T, axis=0)

#     return mfcc


# def analyze_audio(audio):

#     features = extract_features(audio)

#     features = features.reshape(1, -1, 1)

#     prediction = ver_model.predict(features)

#     idx = np.argmax(prediction)

#     confidence = float(np.max(prediction) * 100)

#     return {
#         "emotion": EMOTIONS_MAP[idx],
#         "confidence": confidence
#     }