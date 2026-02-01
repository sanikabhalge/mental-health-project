from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "mindcare-change-in-production-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    database_url: str = "sqlite:///./mindcare.db"

    class Config:
        env_file = ".env"


settings = Settings()
