import json
import scrapy
from urllib.parse import urljoin

from app import settings
from app.items import FlatItem
from app.utils import get_nested_item, part_range


def get_main_description(property_name):
    return f'//*[@data-name="{property_name}"]/*[last()]/text()'


WEBSITE_URL = 'https://krisha.kz'

FLATS_PAGE_URL = settings.FLATS_PAGE_URL
FLATS_PAGINATOR_MAX_PAGE_XPATH = '//a[contains(@class, "paginator__btn")][last() - 1]/@data-page'

FLATS_URLS_XPATH = '//a[contains(@class, "a-card__title")]/@href'
FLATS_PUB_DATES_XPATH = '//div[contains(@class, "card-stats")]/div[2]/text()'

FLAT_TITLE_XPATH = '//div[contains(@class, "offer__advert-title")]/h1/text()'
FLAT_PRICE_XPATH = '//div[contains(@class, "offer__price")]/text()'

BUILDING_WALL_TYPE_XPATH = get_main_description('flat.building')
BUILDING_CONSTRUCTION_YEAR_XPATH = get_main_description('flat.building')
BUILDING_FLOORS_COUNT_XPATH = get_main_description('flat.floor')

FLAT_CEILING_HEIGHT_XPATH = get_main_description('ceiling')
FLAT_FLOOR_XPATH = get_main_description('flat.floor')

SCRIPT_OBJ_XPATH = 'substring-before(substring-after(//*[@id="jsdata"]/text(), "var data = "), ";")'
FLAT_KRISHA_ID_KEY = ['advert', 'id']
FLAT_LONGITUDE_KEY = ['advert', 'map', 'lon']
FLAT_ATTITUDE_KEY = ['advert', 'map', 'lat']
FLAT_TOTAL_AREA_KEY = ['advert', 'square']
FLAT_ROOMS_COUNT_KEY = ['advert', 'rooms']
FLAT_ADDRESS_KEY = ['advert', 'addressTitle']
FLAT_PRICE_KEY = ['advert', 'price']
FLAT_CITY_KEY = ['advert', 'address', 'city']
FLAT_REGION_KEY = ['advert', 'address', 'region']
FLAT_SELLER_USER_TYPE_KEY = ['advert', 'userType']


class FlatSpider(scrapy.Spider):
    name = 'flat_spider'

    def start_requests(self):
        yield scrapy.Request(FLATS_PAGE_URL)

    def get_part(self):
        """Номер интанса при распределенном парсинге"""
        return int(getattr(self, 'part', 0))

    def get_total(self):
        return int(getattr(self, 'total', 1))

    def parse(self, response):
        max_page = int(response.xpath(FLATS_PAGINATOR_MAX_PAGE_XPATH).get())

        for page in part_range(self.get_part(), self.get_total(), range(1, max_page + 1)):
            url = f'{FLATS_PAGE_URL}?page={page}'
            self.logger.warning(f'in page: {url}')
            yield scrapy.Request(url, self.parse_item)

    def parse_item(self, response):
        urls = response.xpath(FLATS_URLS_XPATH).getall()
        pub_dates = response.xpath(FLATS_PUB_DATES_XPATH).getall()

        for idx, flat_url in enumerate(urls):
            full_flat_url = urljoin(WEBSITE_URL, flat_url)
            item = FlatItem(url=full_flat_url, pub_date=pub_dates[idx])
            yield scrapy.Request(full_flat_url, self.parse_details, cb_kwargs={'item': item})

    def parse_details(self, response, item):
        script_obj = json.loads(response.xpath(SCRIPT_OBJ_XPATH).get())

        item['krisha_id'] = get_nested_item(script_obj, FLAT_KRISHA_ID_KEY)
        item['title'] = response.xpath(FLAT_TITLE_XPATH).get()
        item['seller_phone'] = None
        item['views_count'] = None
        item['price'] = get_nested_item(script_obj, FLAT_PRICE_KEY)
        item['rooms_count'] = get_nested_item(script_obj, FLAT_ROOMS_COUNT_KEY)
        item['total_area'] = get_nested_item(script_obj, FLAT_TOTAL_AREA_KEY)
        item['ceiling_height'] = response.xpath(FLAT_CEILING_HEIGHT_XPATH).get()
        item['region'] = get_nested_item(script_obj, FLAT_REGION_KEY)
        item['city'] = get_nested_item(script_obj, FLAT_CITY_KEY)
        item['address'] = get_nested_item(script_obj, FLAT_ADDRESS_KEY)
        item['flat_floor'] = response.xpath(FLAT_FLOOR_XPATH).get()
        item['longitude'] = get_nested_item(script_obj, FLAT_LONGITUDE_KEY)
        item['attitude'] = get_nested_item(script_obj, FLAT_ATTITUDE_KEY)
        item['construction_year'] = response.xpath(BUILDING_CONSTRUCTION_YEAR_XPATH).get()
        item['floors_count'] = response.xpath(BUILDING_FLOORS_COUNT_XPATH).get()
        item['wall_type'] = response.xpath(BUILDING_WALL_TYPE_XPATH).get()
        item['seller_user_type'] = get_nested_item(script_obj, FLAT_SELLER_USER_TYPE_KEY)

        return item
