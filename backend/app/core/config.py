from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "KrishiSampann"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "postgresql://krishisampann:password@localhost:5432/krishisampann"
    
    # Vector database settings
    QDRANT_URL: str = "http://localhost:6335"
    QDRANT_COLLECTION_NAME: str = "krishisampann_knowledge"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI/ML settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # External APIs
    WEATHER_API_KEY: Optional[str] = None
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    MANDI_API_URL: str = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    # Voice settings
    SUPPORTED_LANGUAGES: list = ["hi", "bn", "ta", "te", "mr", "gu", "pa", "or", "ml", "kn"]
    DEFAULT_LANGUAGE: str = "hi"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # Cache settings
    CACHE_TTL: int = 3600  # 1 hour
    
    # Monitoring settings
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
