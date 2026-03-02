"""Application settings configuration."""

import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENV: str = os.getenv("ENV", "develop")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # Application
    APP_NAME: str = "Student Management System"
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "jwt-secret-key-change-in-production"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{Path(__file__).parent.parent.parent}/data/{ENV}.db"
    )

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    class Config:
        """Pydantic config."""

        env_file = f".env.{os.getenv('ENV', 'develop')}"
        case_sensitive = True


settings = Settings()
