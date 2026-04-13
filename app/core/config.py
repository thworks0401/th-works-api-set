"""AppSettings — .envから設定を読み込む"""
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    API_KEY: str = "dev-insecure-key"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# lru_cache を外してインスタンス直生成（キャッシュ問題を排除）
settings = Settings()

# 起動時にAPI_KEYの先頭4文字をログ出力（全体は出さない）
logger.info(f"[config] API_KEY loaded: {settings.API_KEY[:4]}**** (env={settings.APP_ENV})")
