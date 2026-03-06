# from deepface import DeepFace

# def analyze_face(image_path):

#     analysis = DeepFace.analyze(
#         img_path=image_path,
#         actions=["emotion"],
#         enforce_detection=False
#     )

#     dominant = analysis[0]["dominant_emotion"]

#     scores = analysis[0]["emotion"]

#     confidence = float(scores.get(dominant, 0))

#     return {
#         "emotion": dominant,
#         "confidence": confidence
#     }