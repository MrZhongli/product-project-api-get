from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    
    # API Info
    api_title: str = "Animal Management API"
    api_description: str = "API para gestión de animales y razas - Grupo Rafael Moreno"
    api_version: str = "1.0.0"
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    
    # Environment
    environment: str = "development"
    debug: bool = True

    # Upload
    upload_dir: str = Field(..., alias="UPLOAD_DIR")
    max_file_size: int = Field(..., alias="MAX_FILE_SIZE")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "forbid"

settings = Settings()
