import pytest
import respx
import httpx
from polybot.scanner.fetcher import fetch_markets_page, FetchError
from polybot.config import config

@pytest.mark.asyncio
@respx.mock
async def test_fetch_markets_page_success():
    url = f"{config.POLYMARKET_GAMMA_API_BASE}{config.POLYMARKET_MARKETS_PATH}"
    mock_data = [{"id": "1", "question": "Test Market"}]
    respx.get(url).mock(return_value=httpx.Response(200, json=mock_data))
    
    async with httpx.AsyncClient() as client:
        markets = await fetch_markets_page(client)
        assert len(markets) == 1
        assert markets[0]["question"] == "Test Market"

@pytest.mark.asyncio
@respx.mock
async def test_fetch_markets_page_rate_limit():
    url = f"{config.POLYMARKET_GAMMA_API_BASE}{config.POLYMARKET_MARKETS_PATH}"
    respx.get(url).mock(return_value=httpx.Response(429))
    
    async with httpx.AsyncClient() as client:
        with pytest.raises(FetchError, match="Rate limited"):
            await fetch_markets_page(client)

@pytest.mark.asyncio
@respx.mock
async def test_fetch_markets_page_empty():
    url = f"{config.POLYMARKET_GAMMA_API_BASE}{config.POLYMARKET_MARKETS_PATH}"
    respx.get(url).mock(return_value=httpx.Response(200, json=[]))
    
    async with httpx.AsyncClient() as client:
        markets = await fetch_markets_page(client)
        assert markets == []
