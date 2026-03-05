from fastapi import APIRouter,Depends
from schemas import ChatMessageCreate, ChatMessageResponse
from groq import Groq
from config import settings
from auth import get_current_user
from agents.alert_agent import detect_suicide_risk
router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)


@router.post("/message", response_model=ChatMessageResponse)
def send_message(data: ChatMessageCreate,user=Depends(get_current_user)):
    context = []

    if data.text:
        context.append(f"User text: {data.text}")
        risk=detect_suicide_risk(data.text,user)

    if data.mic_on:
        context.append("User microphone is ON.")

    if data.camera_on:
        context.append("User camera is ON.")

    prompt = f"""
You are MindCare Bot, a calm, empathetic psychiatrist assistant.
Your role is to support the user emotionally, not diagnose.

Context:
{chr(10).join(context)}

Respond in a warm, reassuring, non-judgmental way.
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
        print("Groq error:", e)
        reply = "I'm here with you. Can you tell me a bit more?"

    return ChatMessageResponse(reply=reply)
