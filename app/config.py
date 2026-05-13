"""
Configuration module for the Session Manager Service.
Loads environment variables and provides application settings.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic for validation and type checking.
    """
    
    # Database settings
    DATABASE_URL: str
    
    # Application settings
    APP_NAME: str = "Session Manager Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        # Load from .env file
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    Using lru_cache ensures we only load settings once.
    """
    return Settings()
