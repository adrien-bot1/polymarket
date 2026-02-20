import httpx
import logging
from polybot.config import config

logger = logging.getLogger("polybot.scanner.fetcher")

async def fetch_markets():
    """Fetch markets from Polymarket Gamma API."""
    url = f"{config.POLYMARKET_GAMMA_API_BASE}{config.POLYMARKET_MARKETS_PATH}"
    logger.info(f"Fetching markets from {url}")
    # Implementation will follow in next phases
    return []
