import asyncio
import argparse
import logging
from polybot.config import config
from polybot.display.banner import render_banner
from polybot.scheduler.loop import run_scheduler, run_scan
from polybot.scanner.pipeline import ScanPipeline
from polybot.notifier.telegram import TelegramNotifier

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def cli_entry():
    parser = argparse.ArgumentParser(description="PolyBot - Polymarket Closing Window Scanner")
    parser.add_argument("--once", action="store_true", help="Run a single scan and exit")
    parser.add_argument("--dry-run", action="store_true", help="Scan but don't send Telegram messages")
    parser.add_argument("--no-banner", action="store_true", help="Skip the ASCII art")
    parser.add_argument("--log-level", type=str, help="Override log level")
    
    args = parser.parse_args()
    
    if args.log_level:
        config.LOG_LEVEL = args.log_level.upper()
        
    setup_logging()
    
    if not args.no_banner:
        render_banner()
        
    asyncio.run(main(args))

async def main(args):
    logger = logging.getLogger("polybot.main")
    logger.info("Initializing PolyBot...")
    
    if args.once:
        logger.info("Running single scan...")
        pipeline = ScanPipeline()
        notifier = TelegramNotifier()
        await run_scan(pipeline, notifier, dry_run=args.dry_run)
    else:
        logger.info("Starting scheduler loop...")
        await run_scheduler(config, dry_run=args.dry_run)

if __name__ == "__main__":
    cli_entry()
