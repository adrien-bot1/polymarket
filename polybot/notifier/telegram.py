import logging
from telegram import Bot
from polybot.config import config
from polybot.notifier.formatter import format_alert_msg, format_summary_msg

logger = logging.getLogger("polybot.notifier.telegram")

class TelegramNotifier:
    def __init__(self):
        self.bot = None
        if config.TELEGRAM_BOT_TOKEN:
            self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        self.chat_id = config.TELEGRAM_CHAT_ID

    async def send_message(self, text: str):
        if not self.bot or not self.chat_id:
            logger.warning("Telegram bot not configured, skipping message.")
            return
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode="MarkdownV2")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

    async def notify_alerts(self, alerts: list):
        """Send notifications for a list of alerts."""
        if not alerts:
            return
            
        # Send summary first
        # (Assuming we have total and filtered counts from elsewhere, or just simple count)
        summary = format_summary_msg(0, 0, len(alerts)) # Placeholder counts
        await self.send_message(summary)
        
        # Send top 3 alerts to avoid spamming
        for alert in alerts[:3]:
            msg = format_alert_msg(alert)
            await self.send_message(msg)
