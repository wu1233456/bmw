# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem

class Bmw3Spider(scrapy.Spider):
    name = "bmw3"
    allowed_domains = ["'car.autohome.com.cn'"]
    start_urls = ['https://car.autohome.com.cn/pic/series/66.html#pvareaid=3454438']

    def parse(self, response):
        # 不要第0个，从第一个开始[1:]
        uiboxs=response.xpath('//div[@class="uibox"]')[1:]
        for uibox in uiboxs:
            title=uibox.xpath('./div[@class="uibox-title"]/a[1]/text()').get()
            hrefs=uibox.xpath('.//ul/li/a/img/@src').getall()
            # for href in hrefs:
            #     href=response.urljoin(href)
            #     print(href)
            hrefs=list(map(lambda href:response.urljoin(href),hrefs))
            item=BmwItem(title=title,image_urls=hrefs)
            yield item


