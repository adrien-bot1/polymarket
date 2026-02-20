import pytest
import os
import json
from polybot.scanner.scorer import PriceHistoryStore, calculate_score
from datetime import datetime, timedelta, timezone

def test_price_history_store(tmp_path):
    db_file = tmp_path / "test_history.json"
    store = PriceHistoryStore(str(db_file))
    
    market_id = "m1"
    prices = ["0.5", "0.5"]
    
    store.add_price(market_id, prices)
    assert len(store.get_history(market_id)) == 1
    
    store.save()
    assert os.path.exists(db_file)
    
    # Reload
    new_store = PriceHistoryStore(str(db_file))
    assert len(new_store.get_history(market_id)) == 1

def test_calculate_score_basic():
    now = datetime.now(timezone.utc)
    market = {
        "id": "m1",
        "volume": "15000",
        "volume24hr": "2000",
        "outcomePrices": ["0.6", "0.4"],
        "endDate": (now + timedelta(hours=10)).isoformat()
    }
    
    # High volume (30) + Time sensitivity (30) + First scan (10) = 70
    score = calculate_score(market, [])
    assert score >= 60

def test_calculate_score_with_trend():
    now = datetime.now(timezone.utc)
    market = {
        "id": "m1",
        "volume": "1000",
        "volume24hr": "100",
        "outcomePrices": ["0.8", "0.2"],
        "endDate": (now + timedelta(hours=40)).isoformat()
    }
    
    # Old price was 0.5, current is 0.8 -> +60% change
    history = [{"timestamp": "...", "prices": ["0.5", "0.5"]}]
    
    # Low volume (0) + Time sensitivity (10) + Trend (40) = 50
    score = calculate_score(market, history)
    assert score >= 40
