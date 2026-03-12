from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    database_url: str 
    GROQ_API_KEY: str 
    # Optional during local/dev testing.
    # Set `ADB_PATH` in `.env` when you want emergency-call triggering enabled.
    ADB_PATH: str | None = None
    MODEL_PATH :str
    class Config:
        env_file = ".env"


settings = Settings()

