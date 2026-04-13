"""AppSettings — .envから設定を読み込む"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_KEY: str = "dev-insecure-key"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
