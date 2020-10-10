import pytz
import telegram
from datetime import datetime

from app import settings

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)


def send_message(msg):
    msg = f'{datetime.now(pytz.timezone(settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")}: {msg}'
    bot.sendMessage(chat_id=settings.TELEGRAM_CHAT_ID, text=msg)
