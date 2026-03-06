from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    database_url: str

    # Used by alert_agent.py (Groq)
    GROQ_API_KEY: str

    # Used by chat_agent.py (Gemini)
    GEMINI_API_KEY: str 

    # Used by alert_service.py (ADB). Optional if you don't use ADB alerts.
    ADB_PATH: str = ""
    class Config:
        env_file = ".env"


settings = Settings()

