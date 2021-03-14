import scrapy


class SuumoSpider(scrapy.Spider):
    name = 'suumo'
    allowed_domains = ['suumo.jp']
    start_urls = ['http://suumo.jp/']

    def parse(self, response):
        pass
