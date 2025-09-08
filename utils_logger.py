from pathlib import Path
from loguru import logger
import sys

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "project3.log"

logger.remove()
logger.add(sys.stderr, level="INFO",
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level:<8} | {message}")
logger.add(LOG_FILE, level="DEBUG", rotation="500 KB", retention=10, compression="zip")

__all__ = ["logger"]