import datetime
import logging
import scrapy
from operator import getitem

logger = logging.getLogger('flat_serializer')


class ItemSerializer:
    def __init__(self, item):
        self.item = item

    def __getattr__(self, attr):
        return getitem(self.item, attr)


MONTHS_MAP = {
    'янв.': 1,
    'фев.': 2,
    'мар.': 3,
    'апр.': 4,
    'май': 5,
    'июн.': 6,
    'июл.': 7,
    'авг.': 8,
    'сен.': 9,
    'окт.': 10,
    'ноя.': 11,
    'дек.': 12
}


class FlatItemSerializer(ItemSerializer):
    def __getattr__(self, attr):
        if getitem(self.item, attr) is None:
            return None

        if attr == 'title':
            try:
                return self.item['title'].strip()
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'region':
            try:
                return self.item['region'].rstrip('_')
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'flat_floor':
            try:
                return int(self.item['flat_floor'].split('из')[0].strip())
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'floors_count':
            try:
                return int(self.item['floors_count'].split('из')[-1].strip())
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'wall_type':
            try:
                raw = self.item['wall_type'].split(',')[0]
                return raw if 'г.п.' not in raw else None
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'construction_year':
            try:
                raw = self.item['construction_year'].split(',')
                if len(raw) == 2:
                    return int(raw[1].strip().split(' ')[0])
                if 'г.п.' in raw[0]:
                    return int(raw[0].split(' ')[0])
                return None
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'pub_date':
            try:
                if not self.item['pub_date'].strip():
                    return None
                day, month = self.item['pub_date'].strip().split()
                return datetime.date(day=int(day), month=MONTHS_MAP[month], year=datetime.date.today().year)
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        if attr == 'ceiling_height':
            try:
                return float(self.item['ceiling_height'].split(' ')[0])
            except Exception as e:
                logger.error(f'{e} for {self.item} in field: {attr}')
                return None

        return getitem(self.item, attr)


class FlatItem(scrapy.Item):
    # объявление
    krisha_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pub_date = scrapy.Field()
    views_count = scrapy.Field()
    seller_phone = scrapy.Field()
    seller_user_type = scrapy.Field()

    # продажа
    price = scrapy.Field()

    # квартира
    rooms_count = scrapy.Field()
    total_area = scrapy.Field()
    ceiling_height = scrapy.Field()
    description = scrapy.Field()

    # расположение
    region = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    flat_floor = scrapy.Field()
    longitude = scrapy.Field()
    attitude = scrapy.Field()

    # здание
    construction_year = scrapy.Field()
    floors_count = scrapy.Field()
    wall_type = scrapy.Field()
    seller_user_type = scrapy.Field()
