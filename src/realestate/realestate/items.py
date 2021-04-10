# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealestateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SuumoItem(scrapy.Item):
    name = scrapy.Field()
    property_name = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    floor_plan = scrapy.Field()
    age = scrapy.Field()
    balcony = scrapy.Field()
