# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "mysql://flutterdb:123456@localhost:3306/flutterdb"
    upload_dir: str = "app/uploads/images"
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_image_types: list = ["image/jpeg", "image/png", "image/jpg"]
    
    class Config:
        env_file = ".env"

settings = Settings()

