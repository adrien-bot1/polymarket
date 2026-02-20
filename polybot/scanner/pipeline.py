import logging
import asyncio
from typing import List, Dict, Any
from polybot.scanner.fetcher import fetch_all_active_markets
from polybot.scanner.filter import apply_filters
from polybot.scanner.scorer import score_markets, PriceHistoryStore
from polybot.sources.resolver import SourceResolver
from polybot.config import config

logger = logging.getLogger("polybot.scanner.pipeline")

class ScanPipeline:
    def __init__(self):
        self.store = PriceHistoryStore()
        self.resolver = SourceResolver()

    async def run_scan(self) -> List[Dict[str, Any]]:
        """Run the full scanning pipeline."""
        logger.info("Starting pipeline scan...")
        
        # 1. Fetch all active markets
        raw_markets = await fetch_all_active_markets(batch_size=config.BATCH_SIZE)
        if not raw_markets:
            logger.warning("No markets fetched. Ending scan.")
            return []
            
        # 2. Apply filters (Window, Price, Volume)
        filtered_markets = apply_filters(raw_markets)
        if not filtered_markets:
            logger.info("No markets passed filters.")
            return []
            
        # 3. Score markets and update history
        scored_markets = score_markets(filtered_markets, self.store)
        
        # 4. Enrich with external data (only for high scoring ones to save API calls)
        top_alerts = scored_markets[:10]  # Limit to top 10 for enrichment
        for market in top_alerts:
            external_data = await self.resolver.get_external_data(market)
            if external_data:
                market["external_data"] = external_data
                
        logger.info(f"Pipeline scan complete. Found {len(scored_markets)} alerts.")
        return scored_markets
