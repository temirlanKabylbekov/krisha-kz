import scrapy
from urllib.parse import urljoin

from app.items import FlatItem
from app.utils import part_range

WEBSITE_URL = 'https://krisha.kz'

FLATS_PAGE_URL = 'https://krisha.kz/prodazha/kvartiry/pavlodar/'
FLATS_PAGINATOR_MAX_PAGE_XPATH = '//a[contains(@class, "paginator__btn")][last() - 1]/@data-page'

FLAT_URL_XPATH = '//a[contains(@class, "a-card__title")]/@href'

FLAT_TITLE_XPATH = '//div[contains(@class, "offer__advert-title")]/h1/text()'


class FlatSpider(scrapy.Spider):
    name = 'flat_spider'

    def start_requests(self):
        yield scrapy.Request(FLATS_PAGE_URL)

    def parse(self, response):
        max_page = int(response.xpath(FLATS_PAGINATOR_MAX_PAGE_XPATH).get())

        page_range = range(1, max_page + 1)
        if hasattr(self, 'part') and hasattr(self, 'total'):
            page_range = part_range(int(self.part), int(self.total), range(1, max_page + 1))

        for page in page_range:
            yield scrapy.Request(f'{FLATS_PAGE_URL}?page={page}', self.parse_item)

    def parse_item(self, response):
        urls = response.xpath(FLAT_URL_XPATH).getall()
        for flat_url in urls:
            full_flat_url = urljoin(WEBSITE_URL, flat_url)
            yield scrapy.Request(full_flat_url, self.parse_details, cb_kwargs={'item': FlatItem(url=full_flat_url)})

    def parse_details(self, response, item):
        item['title'] = response.xpath(FLAT_TITLE_XPATH).get().strip()
        return item
