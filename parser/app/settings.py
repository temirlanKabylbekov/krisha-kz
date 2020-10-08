import os
from dotenv import load_dotenv

load_dotenv()

# custom settings
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_BATCH_SIZE = os.getenv('DB_BATCH_SIZE')


# scrapy framework settings
BOT_NAME = 'app'

SPIDER_MODULES = ['app.spiders']
NEWSPIDER_MODULE = 'app.spiders'

ITEM_PIPELINES = {
    'app.pipelines.DatabasePipeline': 100,
}

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 100,
}

ROTATING_PROXY_LIST_PATH = 'proxies.txt'
ROTATING_PROXY_LIST = [
    "54.188.85.68:8888",
    "18.237.80.51:8888",
    "54.213.20.203:8888",
    "18.236.139.255:8888",
    "34.219.137.149:8888",
]

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 1
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
REDIRECT_ENABLED = False
