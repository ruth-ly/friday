import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    GUARDIAN_API_KEY: str = os.getenv("GUARDIAN_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    BRAVE_SEARCH_API_KEY: str = os.getenv("BRAVE_SEARCH_API_KEY", "")

    LOG_LEVEL: str = os.getenv("FRIDAY_LOG_LEVEL", "INFO")
    CACHE_TTL: int = int(os.getenv("FRIDAY_CACHE_TTL", "300"))
    MAX_WORKERS: int = int(os.getenv("FRIDAY_MAX_WORKERS", "8"))

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))


config = Config()
