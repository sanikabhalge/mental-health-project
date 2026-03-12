# from agents.alert_agent import detect_suicide_risk
from agents.chat_agent import generate_chat_reply

from agents.emotion_detection_agents.text_analysis import text_emotion
from agents.emotion_detection_agents.audio_emt import analyze_audio_emotion
from agents.emotion_detection_agents.video_emt import analyze_video_emotion


async def process_chat_message(data, user, audio_bytes=None, video_bytes=None):

    text = data.text if data else None
    transcript = None
    emotion_detected = None

    # ---------------- MODE 1 : TEXT ---------------- #

    if text and not audio_bytes and not video_bytes:

        # detect_suicide_risk(text, user)

        emotion_detected = text_emotion(text)

        reply = generate_chat_reply(
            text=text,
            current_emotion=emotion_detected,
            user=user
        )

        return {
            "reply": reply,
            "emotion": emotion_detected
        }

    # ---------------- MODE 2 : AUDIO ---------------- #

    elif audio_bytes and not video_bytes:

        audio_result = analyze_audio_emotion(audio_bytes)

        transcript = audio_result.get("transcript")
        emotion_detected = audio_result.get("emotion")

        # if transcript:
            # detect_suicide_risk(transcript, user)
        print("trnascription ,", transcript)
        reply = generate_chat_reply(
            text=transcript,
            current_emotion=emotion_detected,
            user=user
        )
        print("chat reply",reply)
        return {
            "reply": reply,
            "emotion": emotion_detected,
            "transcript": transcript
        }

    # ---------------- MODE 3 : VIDEO (video + audio) ---------------- #

    elif video_bytes:

        video_result =  analyze_video_emotion(video_bytes)

        transcript = video_result.get("transcript")
        emotion_detected = video_result.get("emotion")

        # if transcript:
            # detect_suicide_risk(transcript, user)

        reply = generate_chat_reply(
            text=transcript,
            current_emotion=emotion_detected,
            user=user
        )

        return {
            "reply": reply,
            "emotion": emotion_detected,
            "transcript": transcript
        }

    # ---------------- FALLBACK ---------------- #

    return {
        "reply": "I'm here with you. Tell me what's on your mind."
    }