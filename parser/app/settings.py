import os
import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# custom settings
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_BATCH_SIZE = os.getenv('DB_BATCH_SIZE')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TIMEZONE = os.getenv('TIMEZONE')
FLATS_PAGE_URL = os.getenv('FLATS_PAGE_URL')

FLAT_TABLE_NAME = lambda: f'flats_{datetime.now(pytz.timezone(TIMEZONE)).strftime("%d_%m_%Y")}'

# scrapy framework settings
BOT_NAME = 'app'

LOG_LEVEL = os.getenv('LOG_LEVEL')

SPIDER_MODULES = ['app.spiders']
NEWSPIDER_MODULE = 'app.spiders'

ITEM_PIPELINES = {
    'app.pipelines.DatabasePipeline': 100,
}

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 100,
}

ROTATING_PROXY_LIST_PATH = 'proxies.txt'

COOKIES_ENABLED = False
DOWNLOAD_DELAY = os.getenv('DOWNLOAD_DELAY')
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
REDIRECT_ENABLED = False
