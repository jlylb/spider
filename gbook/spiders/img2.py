# -*- coding: utf-8 -*-
"""



  Last Modified: 2016/1/22 11:11:38






"""
import scrapy
from gbook.items import ImageItem,ImageDetail,Photo
import urlparse
import json
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
        box = response.css('.uibox')
        items = response.meta['item'];
        detail = []
        for sel in box:
            item = ImageDetail()
            item['name'] = sel.xpath('.//div[contains(@class,"uibox-title")]/a[1]/text()').extract()
            item['image_urls'] = sel.xpath('.//div[contains(@class,"uibox-con")]//li/a/img/@src').extract()
            photos = sel.xpath('.//div[contains(@class,"uibox-con")]//li/a/@href').extract()
            for pic in photos:
                yield scrapy.Request(urlparse.urljoin(self.http_header,pic),meta={"name": item['name'],'title':items['title']},callback = self.parse_photo)
            detail.append(item)

        items['detail']=detail
        yield items
    def parse_photo(self,response):
        item = ImageDetail()
        item['name']=response.meta['name']
        item['title']=response.meta['title']
        item['image_urls']=response.css('.pic>#img::attr("src")').extract()
        yield item

