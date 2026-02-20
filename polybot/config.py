import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    POLYMARKET_GAMMA_API_BASE: str = os.getenv("POLYMARKET_GAMMA_API_BASE", "https://gamma-api.polymarket.com")
    POLYMARKET_EVENTS_PATH: str = os.getenv("POLYMARKET_EVENTS_PATH", "/events")
    POLYMARKET_MARKETS_PATH: str = os.getenv("POLYMARKET_MARKETS_PATH", "/markets")
    SCAN_INTERVAL_HOURS: int = int(os.getenv("SCAN_INTERVAL_HOURS", "2"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "1000"))
    MIN_SCORE: int = int(os.getenv("MIN_SCORE", "20"))
    MIN_VOLUME_TOTAL: float = float(os.getenv("MIN_VOLUME_TOTAL", "1000"))
    MIN_VOLUME_24H: float = float(os.getenv("MIN_VOLUME_24H", "100"))
    PRICE_MIN: float = float(os.getenv("PRICE_MIN", "0.05"))
    PRICE_MAX: float = float(os.getenv("PRICE_MAX", "0.95"))
    WINDOW_MIN_HOURS: int = int(os.getenv("WINDOW_MIN_HOURS", "6"))
    WINDOW_MAX_HOURS: int = int(os.getenv("WINDOW_MAX_HOURS", "72"))
    WUNDERGROUND_API_KEY: str = os.getenv("WUNDERGROUND_API_KEY", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

config = Config()
