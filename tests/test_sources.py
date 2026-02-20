import pytest
from polybot.sources.resolver import SourceResolver

@pytest.mark.asyncio
async def test_source_resolver():
    resolver = SourceResolver()
    
    # Test weather resolution
    market_weather = {"question": "What will be the temperature in NYC?"}
    assert resolver.resolve(market_weather) == "weather"
    
    # Test TSA resolution
    market_tsa = {"question": "How many TSA passengers on Friday?"}
    assert resolver.resolve(market_tsa) == "tsa"
    
    # Test CDC resolution
    market_cdc = {"question": "Will CDC report more flu cases?"}
    assert resolver.resolve(market_cdc) == "cdc"
    
    # Test no resolution
    market_none = {"question": "Will Bitcoin reach 100k?"}
    assert resolver.resolve(market_none) is None

@pytest.mark.asyncio
async def test_get_external_data():
    resolver = SourceResolver()
    market = {"question": "Temperature in London"}
    data = await resolver.get_external_data(market)
    assert data is not None
    assert data["source"] == "wunderground"
