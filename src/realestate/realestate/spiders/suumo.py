import re
from urllib import parse
from datetime import datetime

import scrapy
from scrapy import Request
from dateutil.parser import parse as dateparse

from realestate.items import SuumoItem


class SuumoSpider(scrapy.Spider):
    name = 'suumo'
    allowed_domains = ['suumo.jp']
    start_urls = ['https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13102'
                  '&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1&pn=1']
    # start_urls = ['http://suumo.jp/']
    base_url = 'https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13102' \
               '&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1&pn='

    def parse(self, response):
        # ページングの最大値を取得
        pageList = response.xpath("//ol[@class='pagination-parts']/li/a/text()").extract()[-1]
        for page in range(1, int(pageList)+1):
            yield Request(url=parse.urljoin(self.start_urls[0], self.base_url+str(page)),
                          callback=self.parse_details)

    def parse_details(self, response):
        suumo_item = SuumoItem()

        # タイトル
        name_list = response.xpath("//h2[@class='property_unit-title']/a/text()").extract()

        # 物件名
        property_name_list = response.xpath("//dt[text()='物件名']/following-sibling::dd[1]/text()").extract()

        # 販売値段
        prices = response.xpath("//div[@class='dottable-line']/dl/dd/span/text()").extract()
        price_list = [re.sub("\\D", "", i) for i in prices]

        # 専有面積
        area = response.xpath("//table[@class='dottable-fix']/tbody/tr/td/dl/dt[text()='専有面積']/following-sibling::dd[1]").xpath('string(.)').extract()
        area_list = [re.findall('\\d+.\\d+', i)[0] for i in area]

        # 間取り
        floor_plan_list = response.\
            xpath("//table[@class='dottable-fix']/tbody/tr/td/dl/dt[text()='間取り']/following-sibling::dd[1]/text()").extract()

        # 築年月
        age = response.xpath("//dt[text()='築年月']/following-sibling::dd[1]/text()").extract()
        age_list = [int((datetime.now()-dateparse(i[:4])).days / 365) for i in age]

        # バルコニー
        balcony = response.xpath("//dt[text()='バルコニー']/following-sibling::dd[1]/text()").extract()
        balcony_list = []
        for i in balcony:
            if len(i) == 1:
                balcony_list.append(0)
            else:
                balcony_list.append(re.findall("\\d+", i)[0])
        for name, property, price, area, floor_plan, age, balcony in\
                zip(name_list, property_name_list, price_list, area_list, floor_plan_list, age_list, balcony_list):
            suumo_item["name"] = name
            suumo_item["property_name"] = property
            suumo_item["price"] = price
            suumo_item["area"] = re.sub("m2", "", area)
            suumo_item["floor_plan"] = floor_plan
            suumo_item["age"] = age
            suumo_item["balcony"] = balcony

            yield suumo_item
