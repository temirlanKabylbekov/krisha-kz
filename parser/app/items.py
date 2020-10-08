import scrapy


class FlatItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
