import logging
from datetime import datetime, timezone
from typing import List, Dict, Any
from polybot.config import config

logger = logging.getLogger("polybot.scanner.filter")

def is_in_window(market: Dict[str, Any]) -> bool:
    """Check if the market resolution is within the target window."""
    end_date_str = market.get("endDate")
    if not end_date_str:
        return False
        
    try:
        # Polymarket dates are usually ISO format
        end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        
        diff = end_date - now
        hours_remaining = diff.total_seconds() / 3600
        
        return config.WINDOW_MIN_HOURS <= hours_remaining <= config.WINDOW_MAX_HOURS
    except Exception as e:
        logger.error(f"Error parsing date for market {market.get('id')}: {e}")
        return False

def is_price_in_range(market: Dict[str, Any]) -> bool:
    """Check if the current market price is within the target range."""
    # Gamma API often provides prices in 'outcomePrices' or 'bestBid'/'bestAsk'
    # For simplicity, we check if there are prices and if they meet the criteria
    prices = market.get("outcomePrices")
    if not prices or not isinstance(prices, list):
        return False
        
    try:
        for price_str in prices:
            price = float(price_str)
            if config.PRICE_MIN <= price <= config.PRICE_MAX:
                return True
        return False
    except (ValueError, TypeError):
        return False

def has_sufficient_volume(market: Dict[str, Any]) -> bool:
    """Check if the market has enough total and 24h volume."""
    total_volume = float(market.get("volume", 0))
    volume_24h = float(market.get("volume24hr", 0))
    
    return total_volume >= config.MIN_VOLUME_TOTAL and volume_24h >= config.MIN_VOLUME_24H

def apply_filters(markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply all filters to a list of markets."""
    filtered = []
    for market in markets:
        if is_in_window(market) and is_price_in_range(market) and has_sufficient_volume(market):
            filtered.append(market)
            
    logger.info(f"Filtered {len(markets)} markets down to {len(filtered)}")
    return filtered
