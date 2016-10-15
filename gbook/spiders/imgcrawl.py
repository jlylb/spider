# -*- coding: utf-8 -*-
"""



  Last Modified: 2016/1/22 16:09:32




"""
#import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gbook.items import ImageItem
class ImgcrawlSpider(CrawlSpider):
    name = 'imgcrawl'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['http://car.autohome.com.cn/pic/']

    rules = (
        Rule(LinkExtractor(allow=(r'brand-\d+\.html',),restrict_xpaths=('//div[@id="cartree"]/ul/li/a/@href')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        img = ImageItem()
        img['image_urls'] = response.css(".uibox li img::attr('src')").extract()
        return img
