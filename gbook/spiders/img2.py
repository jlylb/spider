# -*- coding: utf-8 -*-
"""



  Last Modified: 2016/1/22 11:11:38






"""
import scrapy
from gbook.items import ImageItem,ImageDetail,Photo
import urlparse
#from scrapy.loader import ItemLoader
#from scrapy.loader.processors import TakeFirst, MapCompos, Join

class Img2Spider(scrapy.Spider):

    name="img2"

    allowed_domains = ["autohome.com.cn"]

    http_header = "http://car.autohome.com.cn"

    start_urls = (
        'http://car.autohome.com.cn/pic',
    )

    def parse(self, response):
        url_start = response.css('.cartree script::attr("src")').extract()
        if url_start:
            yield scrapy.Request(urlparse.urljoin(self.http_header,url_start[0]),callback = self.parse_brand)

    def parse_brand(self, response):
        item_info=response.css('ul li h3 a::attr("href")').extract()
        if item_info:
            for href in item_info:
                yield scrapy.Request(urlparse.urljoin(self.http_header,href),callback = self.parse_serie)

    def parse_serie(self, response):

        info = response.css(".uibox li")
        for xx in info:
            item = ImageItem()
            item['title'] = xx.css('span a::text').extract()[0]
            item['pic_num'] = xx.css('span::text').extract()[0]
            item['href'] = xx.css('a img::attr("src")').extract()[0]
            detail = xx.xpath('./a/@href').extract()[0]
            yield scrapy.Request(urlparse.urljoin(self.http_header,detail),meta={"item": item},callback = self.parse_detail)

    def parse_detail(self, response):
        item = ImageDetail()
        item['name'] = response.css('.cartab-title h2>a::text').extract()
        item['img_type'] = response.css('.uibox .uibox-title>a:first-child::text').extract()
        item['img_type_url'] = response.css('.uibox-con li a>img::attr("src")').extract()
        items = response.meta['item'];
        items['detail']=item
        return items
