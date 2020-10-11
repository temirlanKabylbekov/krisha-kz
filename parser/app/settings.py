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
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TIMEZONE = os.getenv('TIMEZONE')
FLATS_PAGE_URL = os.getenv('FLATS_PAGE_URL')
TELEGRAM_NOTIFICATIONS = os.getenv('TELEGRAM_NOTIFICATIONS') == 'on'

FLATS_URLS = [
    'https://krisha.kz/prodazha/kvartiry/almaty/',
    'https://krisha.kz/prodazha/kvartiry/vostochno-kazahstanskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/nur-sultan/',
    'https://krisha.kz/prodazha/kvartiry/shymkent/',
    'https://krisha.kz/prodazha/kvartiry/akmolinskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/aktjubinskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/almatinskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/atyrauskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/zhambylskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/zapadno-kazahstanskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/karagandinskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/kostanajskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/kyzylordinskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/mangistauskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/pavlodarskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/severo-kazahstanskaja-oblast/',
    'https://krisha.kz/prodazha/kvartiry/juzhno-kazahstanskaja-oblast/'
]
if FLATS_PAGE_URL:
    FLATS_URLS = [FLATS_PAGE_URL]


FLAT_TABLE_NAME = os.getenv('TABLE_NAME')

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
