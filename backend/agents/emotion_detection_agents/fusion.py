def fuse_emotions(audio_emotion, video_emotion, audio_conf=0.0, video_conf=0.0):

    # fallback cases
    if not audio_emotion and not video_emotion:
        return "neutral", 0.5

    if audio_emotion and not video_emotion:
        return audio_emotion, audio_conf

    if video_emotion and not audio_emotion:
        return video_emotion, video_conf

    # if both emotions agree
    if audio_emotion == video_emotion:
        confidence = (audio_conf + video_conf) / 2
        return audio_emotion, confidence

    # weighted fusion
    audio_weight = 0.6
    video_weight = 0.4

    audio_score = audio_conf * audio_weight
    video_score = video_conf * video_weight

    if audio_score >= video_score:
        return audio_emotion, audio_score
    else:
        return video_emotion, video_score