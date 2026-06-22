import sys
from loguru import logger
from src.core.config import config

logger.remove()
logger.add(
    sys.stderr,
    level=config.LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - {message}",
)
logger.add(
    "data/logs/friday.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
)
