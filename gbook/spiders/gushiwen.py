# -*- coding: utf-8 -*-
import scrapy
import urlparse


class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/guwen']

    def parse(self, response):
        hrefs=response.css('.titletype .son2 .sright a::attr(href)').extract()
        for url in [hrefs[0]]:
            url=urlparse.urljoin(self.start_urls[0],url)
            yield scrapy.Request(url,callback=self.parse_type)


    def parse_type(self, response):
        hrefs=response.css('.sonspic .cont p a:first-child::attr(href)').extract()
        for url in hrefs:
            url=urlparse.urljoin(self.start_urls[0],url)
            yield scrapy.Request(url,callback=self.parse_list)


    def parse_list(self, response):
        hrefs=response.css('.bookcont a::attr(href)').extract()
        for url in hrefs:
            url=urlparse.urljoin(self.start_urls[0],url)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        title=response.css('.cont h1 b::text').extract_first()
        author=response.css('.cont .source a::text').extract_first()
        content=response.css('.cont .contson p').extract()
        yield {'title':title,'author':author,'content':''.join(content)}
