import pytest
from datetime import datetime, timedelta, timezone
from polybot.scanner.filter import is_in_window, is_price_in_range, has_sufficient_volume
from polybot.config import config

def test_is_in_window():
    now = datetime.now(timezone.utc)
    
    # Within window (e.g., 24 hours)
    market_ok = {"endDate": (now + timedelta(hours=24)).isoformat()}
    assert is_in_window(market_ok) is True
    
    # Below min (e.g., 3 hours)
    market_too_soon = {"endDate": (now + timedelta(hours=3)).isoformat()}
    assert is_in_window(market_too_soon) is False
    
    # Above max (e.g., 80 hours)
    market_too_far = {"endDate": (now + timedelta(hours=80)).isoformat()}
    assert is_in_window(market_too_far) is False
    
    # Past
    market_past = {"endDate": (now - timedelta(hours=1)).isoformat()}
    assert is_in_window(market_past) is False

def test_is_price_in_range():
    # OK
    assert is_price_in_range({"outcomePrices": ["0.10", "0.90"]}) is True
    # Edge cases
    assert is_price_in_range({"outcomePrices": [str(config.PRICE_MIN)]}) is True
    assert is_price_in_range({"outcomePrices": [str(config.PRICE_MAX)]}) is True
    # Out of range
    assert is_price_in_range({"outcomePrices": ["0.01"]}) is False
    assert is_price_in_range({"outcomePrices": ["0.99"]}) is False
    # Missing data
    assert is_price_in_range({}) is False

def test_has_sufficient_volume():
    # OK
    assert has_sufficient_volume({"volume": "1500", "volume24hr": "200"}) is True
    # Low total
    assert has_sufficient_volume({"volume": "500", "volume24hr": "200"}) is False
    # Low 24h
    assert has_sufficient_volume({"volume": "1500", "volume24hr": "50"}) is False
