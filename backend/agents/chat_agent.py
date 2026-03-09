from groq import Groq
from config import settings

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)


def generate_chat_reply(text: str, current_emotion, user=None):
    """
    Generates an empathetic mental health response.
    
    Args:
        text: User message text
        current_emotion: dict with emotion and confidence, or string
        user: User object
        
    Returns:
        LLM-generated response string
    """

    # -------- Process emotion data --------
    emotion_text = "unknown"
    confidence_score = 0
    
    if current_emotion:
        if isinstance(current_emotion, dict):
            emotion_text = current_emotion.get("emotion", "unknown")
            confidence_score = current_emotion.get("confidence", 0)
        elif isinstance(current_emotion, str):
            emotion_text = current_emotion
    
    emotion_summary = f"{emotion_text} (confidence: {confidence_score:.1f}%)" if confidence_score else emotion_text
    emotion_trend_summary = "no data yet"  # TODO: emotion trend analysis from database

    user_age = user.age if user else "unknown"
    user_gender = user.gender if user else "unknown"

    # -------- Prompt --------
    prompt = f"""
You are MindCare Bot, a calm and empathetic mental health assistant.

Your role:
- Listen carefully to the user
- Provide emotional support
- Encourage healthy coping
- Never diagnose medical conditions

User Profile:
Age: {user_age}
Gender: {user_gender}

Current Emotion (detected):
{emotion_summary}

Emotion Trend Summary:
{emotion_trend_summary}

User Message:
{text}

Respond with empathy, warmth, and encouragement.
Avoid sounding robotic or overly clinical.
Keep responses concise (2-3 sentences).
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        reply = completion.choices[0].message.content

    except Exception as e:
        print("Chat Agent Groq Error:", e)
        reply = "I'm here with you. Would you like to share a little more about how you're feeling?"

    return reply