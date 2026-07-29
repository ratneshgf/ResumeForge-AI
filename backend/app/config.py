"""
Central app settings, loaded from environment variables (.env).
Uses pydantic-settings so every config value is typed and documented in
one place instead of scattered os.getenv() calls.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "ResumeForge AI"
    ENV: str = "development"

    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    # AI providers
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    AI_PROVIDER: str = "gemini"  # "gemini" or "openai"
    
    # AI Configuration
    AI_MAX_RETRIES: int = 3
    AI_TIMEOUT_SECONDS: int = 30
    AI_TEMPERATURE: float = 0.7

    # Razorpay
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    # Redis (for session store and rate limiting)
    REDIS_URL: str = "redis://localhost:6379/0"
    USE_REDIS: bool = False  # Set to True in production

    # Storage
    UPLOAD_DIR: str = "storage/uploads"
    TEMP_DIR: str = "storage/temp"
    OUTPUT_DIR: str = "storage/output"
    MAX_UPLOAD_MB: int = 5
    FILE_TTL_MINUTES: int = 60

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 30

    # NLP Models
    SPACY_MODEL: str = "en_core_web_md"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()
