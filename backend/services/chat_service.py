from agents.alert_agent import detect_suicide_risk
from agents.chat_agent import generate_chat_reply
from agents.emotion_detection_agents.text_analysis import text_emotion
# from agents.emotion_detection_agents.audio_emt import analyze_audio
# from agents.emotion_detection_agents.video_emt import analyze_face
# from agents.emotion_detection_agents.fusion import fuse_emotions

def process_chat_message(data, user):
    """
    Handles chat logic before sending to the LLM agent.
    """

    text = data.text or ""
    # -------- Suicide risk detection --------
    if text:
        detect_suicide_risk(text, user)
        
    # -------- Determine interaction mode --------
    if text and not data.mic_on and not data.camera_on:
        emotion_detected=text_emotion(text)
        print("text emtion detected : ",emotion_detected)
        mode = 1  # text only

    # elif data.mic_on and not data.camera_on:
    #     emotion_detected=analyze_audio(data.mic_on)
    #     mode = 2  # mic only

    # elif text and data.camera_on and not data.mic_on:
    #     text_emt=text_emotion(text)
    #     face_emt=analyze_face(data.camera_on)
    #     emotion_detected=fuse_emotions(text=text_emt,video=face_emt)
    #     mode = 3  # text + video

    # elif data.mic_on and data.camera_on:
    #     audio_emt=analyze_audio(data.mic_on)
    #     face_emt=analyze_face(data.camera_on)
    #     emotion_detected=fuse_emotions(audio=audio_emt,video=face_emt)
    #     mode = 4  # mic + video

    else:
        mode = 1

    

    # -------- Send to chat agent --------
    reply = generate_chat_reply(
        text=text,
        current_emotion=emotion_detected,
        user=user
    )

    return reply