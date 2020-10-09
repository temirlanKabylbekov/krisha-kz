import logging
import scrapy
import unicodedata

logger = logging.getLogger('flat_serializer')


class FlatItem(scrapy.Item):
    # объявление
    krisha_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pub_date = scrapy.Field()
    views_count = scrapy.Field()

    # продажа
    price = scrapy.Field()

    # квартира
    rooms_count = scrapy.Field()
    total_area = scrapy.Field()
    living_area = scrapy.Field()
    kitchen_area = scrapy.Field()
    condition = scrapy.Field()
    bathroom = scrapy.Field()
    balcony = scrapy.Field()

    # расположение
    region = scrapy.Field()
    address = scrapy.Field()
    floor = scrapy.Field()

    # здание
    construction_year = scrapy.Field()
    floors_count = scrapy.Field()

    @property
    def serialized_title(self):
        return self['title'].strip()

    @property
    def serialized_url(self):
        return self['url']

    @property
    def serialized_price(self):
        try:
            return float(unicodedata.normalize('NFKD', self['price'].strip()).replace(' ', ''))
        except ValueError as e:
            logger.error(f'{e} for {self["url"]}')
            return 0
