import httpx
import logging
import asyncio
from typing import List, Dict, Any, Optional
from polybot.config import config

logger = logging.getLogger("polybot.scanner.fetcher")

class FetchError(Exception):
    """Custom exception for fetcher related errors."""
    pass

async def fetch_markets_page(client: httpx.AsyncClient, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Fetch a single page of markets from Polymarket Gamma API."""
    url = f"{config.POLYMARKET_GAMMA_API_BASE}{config.POLYMARKET_MARKETS_PATH}"
    params = {
        "limit": limit,
        "offset": offset,
        "active": "true",
        "closed": "false"
    }
    
    try:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning(f"Rate limited (429). Retrying after delay...")
            raise FetchError("Rate limited")
        logger.error(f"HTTP error fetching markets: {e}")
        raise FetchError(f"HTTP error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Unexpected error fetching markets: {e}")
        raise FetchError(f"Unexpected error: {e}")

async def fetch_all_active_markets(batch_size: int = 100) -> List[Dict[str, Any]]:
    """Fetch all active markets using pagination."""
    all_markets = []
    offset = 0
    
    async with httpx.AsyncClient() as client:
        while True:
            logger.info(f"Fetching markets batch: offset={offset}, limit={batch_size}")
            try:
                markets = await fetch_markets_page(client, limit=batch_size, offset=offset)
                if not markets:
                    logger.info("No more markets found. Fetching complete.")
                    break
                
                all_markets.extend(markets)
                logger.info(f"Fetched {len(markets)} markets. Total: {len(all_markets)}")
                
                if len(markets) < batch_size:
                    logger.info("Reached end of markets list.")
                    break
                    
                offset += batch_size
                # Small delay to be polite to the API
                await asyncio.sleep(0.1)
                
            except FetchError as e:
                if "Rate limited" in str(e):
                    await asyncio.sleep(5)
                    continue
                logger.error(f"Stopping fetch due to error: {e}")
                break
                
    return all_markets
