from typing import Optional, Dict, Any
from polybot.sources.wunderground import WundergroundSource
from polybot.sources.tsa import TSASource
from polybot.sources.cdc import CDCSource

class SourceResolver:
    def __init__(self):
        self.sources = {
            "weather": WundergroundSource(),
            "tsa": TSASource(),
            "cdc": CDCSource()
        }

    def resolve(self, market: Dict[str, Any]) -> Optional[str]:
        """Determine which data source is relevant for a market."""
        question = market.get("question", "").lower()
        if "temperature" in question or "weather" in question or "rain" in question:
            return "weather"
        if "tsa" in question or "passengers" in question:
            return "tsa"
        if "flu" in question or "cdc" in question or "cases" in question:
            return "cdc"
        return None

    async def get_external_data(self, market: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        source_type = self.resolve(market)
        if source_type and source_type in self.sources:
            return await self.sources[source_type].fetch_data(market.get("question", ""))
        return None
