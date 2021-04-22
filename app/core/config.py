import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = str(os.environ.get("SECRET_KEY"))
    CORS_ALLOW_ORIGINS: List[str] = []
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///sqlite.db"
    )
    SQLALCHEMY_ECHO: bool = os.environ.get("SQLALCHEMY_ECHO", False)

    class Config:
        case_sensitive = True


settings = Settings()
