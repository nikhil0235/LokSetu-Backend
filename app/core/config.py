from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "super-secret"
    EXCEL_DIR: str = "app/data/constituency_files"
    EXCEL_CACHE_TTL: int = 60  # seconds

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM: str = "noreply@example.com"
    
    class Config:
        env_file = ".env"

settings = Settings()
