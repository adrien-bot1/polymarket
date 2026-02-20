import logging
from telegram import Bot
from polybot.config import config

logger = logging.getLogger("polybot.notifier.telegram")

class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        self.chat_id = config.TELEGRAM_CHAT_ID

    async def send_message(self, text: str):
        if not config.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram token not set, skipping notification.")
            return
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode="MarkdownV2")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
