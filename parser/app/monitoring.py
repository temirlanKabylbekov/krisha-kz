import pytz
import telegram
from datetime import datetime
from functools import lru_cache

from app import settings


@lru_cache(maxsize=None)
def get_client():
    if not settings.TELEGRAM_NOTIFICATIONS:
        return None
    return telegram.Bot(token=settings.TELEGRAM_TOKEN)


def send_message(msg):
    if not settings.TELEGRAM_NOTIFICATIONS:
        return

    msg = f'{datetime.now(pytz.timezone(settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")}: {msg}'
    get_client().sendMessage(chat_id=settings.TELEGRAM_CHAT_ID, text=msg)
