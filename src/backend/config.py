"""
Configuración de la aplicación
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic"""
    
    # API Keys
    OPENAI_API_KEY: str
    USDA_API_KEY: str
    NUTRITIONIX_APP_ID: str
    NUTRITIONIX_APP_KEY: str
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/contador_calorias"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # ML Service
    ML_TIMEOUT: int = 30  # seconds
    ML_MAX_RETRIES: int = 3
    
    # File Upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()