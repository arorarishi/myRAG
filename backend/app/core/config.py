from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Framework"
    PROJECT_VERSION: str = "0.1.0"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]  # Vite default port

    class Config:
        case_sensitive = True

settings = Settings()
