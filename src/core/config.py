import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # LLM
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # News
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    GUARDIAN_API_KEY: str = os.getenv("GUARDIAN_API_KEY", "")

    # Search
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

    # Voice — ElevenLabs primary
    ELEVENLABS_API_KEY: str  = os.getenv("ELEVENLABS_API_KEY", "")
    # "Rachel" voice — calm, professional, closest to Friday's tone
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    OPENAI_API_KEY: str      = os.getenv("OPENAI_API_KEY", "")

    # App
    LOG_LEVEL: str  = os.getenv("FRIDAY_LOG_LEVEL", "INFO")
    CACHE_TTL: int  = int(os.getenv("FRIDAY_CACHE_TTL", "300"))
    MAX_WORKERS: int = int(os.getenv("FRIDAY_MAX_WORKERS", "8"))

    # Server
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))


config = Config()
