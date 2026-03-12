from config import settings
from groq import Groq
from services.alert_service import trigger_alert
def detect_suicide_risk(text: str,user) -> bool:
    client = Groq(api_key=settings.GROQ_API_KEY)
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=
                [{"role": "system",  "content": """
                                                    You are a text classifier.

                                                    Your task is ONLY to classify the user's message.

                                                    If the message contains suicidal thoughts, self-harm intent, or desire to die, respond exactly:

                                                    YES

                                                    Otherwise respond exactly:

                                                    NO

                                                    Do not give advice.
                                                    Do not explain.
                                                    Do not add extra words.
                                                    Only output YES or NO.
                                                    """},
                {"role":"user","content":text}
            ],
            temperature=0,
        )
        reply = completion.choices[0].message.content.strip().lower()
        print("Alert Agent LLM reply:", reply)
        
    except Exception as e:
        print("GROQ ALERT AGENT ERROR:", str(e))
        return False
    
    if "yes" in reply:
        trigger_alert(user,text)
    
    else : 
        return False