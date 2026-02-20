import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("polybot.scheduler")

async def run_scan():
    logger.info("Starting market scan...")
    # TODO: Implement the full scan pipeline
    await asyncio.sleep(2)
    logger.info("Scan complete.")

async def run_scheduler(config):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_scan, 'interval', hours=config.SCAN_INTERVAL_HOURS)
    
    logger.info(f"Scheduled scan every {config.SCAN_INTERVAL_HOURS} hours.")
    scheduler.start()
    
    # Run one immediate scan
    await run_scan()
    
    try:
        # Keep the loop alive
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Scheduler stopped.")
        scheduler.shutdown()
