from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """CMS Mock Service Settings"""

    app_name: str = "CMS Mock Service"
    host: str = "0.0.0.0"
    port: int = 3001
    debug: bool = True

    # CORS settings
    cors_origins: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
