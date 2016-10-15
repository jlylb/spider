# -*- coding: utf-8 -*-
"""



  Last Modified: 2016/1/22 11:11:38






"""
import scrapy
from gbook.items import ImageItem,ImageDetail,Photo

class ImageSpider(scrapy.Spider):

    name="image"

    allowed_domains = ["autohome.com.cn"]

    http_header = "http://car.autohome.com.cn"

    start_urls = (
        'http://car.autohome.com.cn/pic',
    )

    def parse(self, response):
        url_start = response.css('.cartree script::attr("src")').extract()
        if url_start:
            yield scrapy.Request(self.http_header+url_start[0],callback = self.parse_brand)

    def parse_brand(self, response):
        item_info=response.css('ul li h3 a::attr("href")').extract()
        if item_info:
            for href in item_info:
                yield scrapy.Request(self.http_header+href,callback = self.parse_serie)

    def parse_serie(self, response):
        item = ImageItem()
        #item['image_urls'] = response.css(".uibox li img::attr('src')").extract()
        info = response.css(".uibox li")
        for xx in info:
            item['title'] = xx.css('span a::text').extract()[0]
            item['pic_num'] = xx.css('span::text').extract()[0]
            item['href'] = xx.css('a img::attr("src")').extract()[0]
            yield item
        for yy in response.css(".uibox li a::attr('href')").extract():
            yield scrapy.Request(self.http_header+yy,callback = self.parse_detail)



    def parse_detail(self, response):
        item = ImageDetail()
        item['name'] = response.css('.cartab-title h2>a::text').extract()
        item['img_type'] = response.css('.uibox .uibox-title>a:first-child::text').extract()
        item['img_type_url'] = response.css('.uibox-con li a>img::attr("src")').extract()
        for xx in  response.css('.uibox-con li a::attr("href")').extract():
            yield scrapy.Request(self.http_header+xx,callback = self.parse_big_photo)
        yield item

    def parse_big_photo(self, response):
        item = Photo()
        item['photo'] = response.css('.pic>img::attr("src")').extract()[0]
        yield item

