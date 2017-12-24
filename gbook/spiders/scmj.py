# -*- coding: utf-8 -*-
import scrapy
import os
from gbook.items import ShiciItem
#import codecs



class ScmjSpider(scrapy.Spider):
    name = "scmj"
    allowed_domains = ["shicimingju.com"]
    start_urls = (
        'http://www.shicimingju.com/',
    )

    def parse(self, response):
        categorys = response.css('.left_mark')[0].css('ul>li>a')
        #for category in categorys:
        #    link = category.css('::attr(href)').extract_first()
        #    #eng_link = os.path.split('/')[-1]
        #    #text = category.css('::text').extract_first()
        #    url = os.path.join(self.start_urls[0],link[1:-1])
        #    yield scrapy.Request(url, self.parse_list)
        link = categorys[0].css('::attr(href)').extract_first()
        self.logger.info('current url is: %s', link)
        #eng_link = os.path.split('/')[-1]
        #text = category.css('::text').extract_first()
        url = os.path.join(self.start_urls[0],link[1:])
        self.logger.info('current url is: %s', url)
        yield scrapy.Request(url, callback = self.parse_list)

    def parse_list(self,response):
        links = response.css('.shirenlist>ul>li>a')
        ls = response.css('.shirenlist')
        for href in links:
            link = href.css('::attr(href)').extract_first()
            #text = href.css('::text').extract_first()
            url = os.path.join(self.start_urls[0],link[1:])
            yield scrapy.Request(url, callback = self.parse_list_zuozhe)
        nextpage = response.css('.pagenavi>span').xpath('a[last()]')
        print nextpage.xpath('text()').extract_first()
        if nextpage.xpath('text()').extract_first()==u'下一页':
            page = nextpage.xpath('@href').extract_first()
            url = os.path.join(self.start_urls[0],page[1:])
            yield scrapy.Request(url, callback = self.parse_list)

    def parse_list_zuozhe(self,response):
        links = response.css('.shicilist>ul').xpath('.//li[1]/a')
        for href in links:
            link = href.css('::attr(href)').extract_first()
            #text = href.css('::text').extract_first()
            url = os.path.join(self.start_urls[0],link[1:])
            yield scrapy.Request(url, callback = self.parse_detail)
        nextpage = response.css('.pagenavi>span').xpath('a[last()]')
        if nextpage.xpath('text()').extract_first()==u'下一页':
            page = nextpage.xpath('@href').extract_first()
            url = os.path.join(self.start_urls[0],page[1:])
            yield scrapy.Request(url, callback = self.parse_list_zuozhe)

    def parse_detail(self,response):
        item = ShiciItem()
        item['title'] = response.css('.zhuti>h2::text').extract_first()[1:-1]
        (category,author) = response.css('.zhuti>.jjzz>a::text').extract()
        item['category'] = category.strip()
        item['author'] = author
        item['content'] = '\n'.join(response.css('.zhuti>.shicineirong::text').extract())
        item['zhujie'] = '\n'.join(response.css('.shangxi::text').extract())
        yield item







