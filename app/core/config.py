from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "ChatOps-Bob Gateway"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # IBM Watsonx AI
    WATSONX_API_URL: str = "https://us-south.ml.cloud.ibm.com"
    WATSONX_PROJECT_ID: str = ""
    IBM_CLOUD_API_KEY: str = ""
    WATSONX_MODEL: str = "ibm/granite-8b-code-instruct"
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/chatops.db"
    
    # AI Configuration
    USE_MOCK_AI: bool = True
    FORCE_ENGLISH_OUTPUT: bool = True  # Force all AI responses to be in English
    
    # Liva Gateway
    LIVA_GATEWAY_URL: str = "http://localhost:8082"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Made with Bob
