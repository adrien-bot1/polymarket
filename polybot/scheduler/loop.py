import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from polybot.scanner.pipeline import ScanPipeline
from polybot.display.cards import render_alert_card, render_scan_summary
from polybot.notifier.telegram import TelegramNotifier
from polybot.notifier.formatter import format_summary_msg

logger = logging.getLogger("polybot.scheduler")

async def run_scan(pipeline: ScanPipeline, notifier: TelegramNotifier, dry_run: bool = False):
    logger.info("Starting scheduled market scan...")
    try:
        alerts = await pipeline.run_scan()
        
        # Display results in terminal
        # (We don't have total/filtered here easily without modifying run_scan, 
        # let's just show alerts for now)
        for alert in alerts:
            render_alert_card(alert)
            
        # Send notifications
        if not dry_run:
            await notifier.notify_alerts(alerts)
            
        logger.info(f"Scan complete. {len(alerts)} alerts processed.")
    except Exception as e:
        logger.error(f"Error during scheduled scan: {e}", exc_info=True)

async def run_scheduler(config, dry_run: bool = False):
    pipeline = ScanPipeline()
    notifier = TelegramNotifier()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_scan, 
        'interval', 
        hours=config.SCAN_INTERVAL_HOURS,
        args=[pipeline, notifier, dry_run]
    )
    
    logger.info(f"Scheduled scan every {config.SCAN_INTERVAL_HOURS} hours.")
    scheduler.start()
    
    # Run one immediate scan
    await run_scan(pipeline, notifier, dry_run)
    
    try:
        # Keep the loop alive
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Scheduler stopped.")
        scheduler.shutdown()
