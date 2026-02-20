import logging
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from polybot.config import config

logger = logging.getLogger("polybot.scanner.scorer")

class PriceHistoryStore:
    def __init__(self, filepath: str = "data/price_history.json"):
        self.filepath = filepath
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    self.history = json.load(f)
            except Exception as e:
                logger.error(f"Error loading price history: {e}")
                self.history = {}
        else:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def save(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.history, f)
        except Exception as e:
            logger.error(f"Error saving price history: {e}")

    def add_price(self, market_id: str, prices: List[float]):
        if market_id not in self.history:
            self.history[market_id] = []
        
        self.history[market_id].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prices": prices
        })
        
        # Keep only last 100 entries per market to save space
        if len(self.history[market_id]) > 100:
            self.history[market_id] = self.history[market_id][-100:]

    def get_history(self, market_id: str) -> List[Dict[str, Any]]:
        return self.history.get(market_id, [])

def calculate_score(market: Dict[str, Any], history: List[Dict[str, Any]]) -> int:
    """Calculate a score from 0-100 for a market."""
    score = 0
    
    # Helper to get prices safely
    from polybot.scanner.filter import get_prices
    current_prices = get_prices(market)
    
    # 1. Volume Score (up to 30 points)
    try:
        total_vol = float(market.get("volume", 0) or 0)
        vol_24h = float(market.get("volume24hr", 0) or 0)
    except (ValueError, TypeError):
        total_vol = 0
        vol_24h = 0
    
    if total_vol > 10000: score += 15
    elif total_vol > 5000: score += 10
    
    if vol_24h > 1000: score += 15
    elif vol_24h > 500: score += 10
    
    # 2. Price Trend Score (up to 40 points)
    if len(history) >= 1 and current_prices:
        try:
            current_price = current_prices[0]
            old_price = float(history[0]["prices"][0])
            
            if old_price > 0:
                change = (current_price - old_price) / old_price
                if abs(change) > 0.2: score += 40
                elif abs(change) > 0.1: score += 20
        except (IndexError, ValueError, ZeroDivisionError):
            pass
    else:
        # First scan bonus
        score += 10
        
    # 3. Time Sensitivity (up to 30 points)
    end_date_str = market.get("endDate")
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
            hours_left = (end_date - datetime.now(timezone.utc)).total_seconds() / 3600
            
            if hours_left < 12: score += 30
            elif hours_left < 24: score += 20
            elif hours_left < 48: score += 10
        except Exception:
            pass
            
    return min(score, 100)

def score_markets(markets: List[Dict[str, Any]], store: PriceHistoryStore) -> List[Dict[str, Any]]:
    """Score all filtered markets and update history."""
    scored_markets = []
    from polybot.scanner.filter import get_prices
    
    for market in markets:
        market_id = market.get("id", "unknown")
        history = store.get_history(market_id)
        
        score = calculate_score(market, history)
        market["score"] = score
        
        # Update history for next time
        store.add_price(market_id, get_prices(market))
        
        if score >= config.MIN_SCORE:
            scored_markets.append(market)
            
    store.save()
    return sorted(scored_markets, key=lambda x: x["score"], reverse=True)
