# -*- coding: utf-8 -*-
import scrapy
import urlparse


class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/guwen/']

    def parse(self, response):
        #hrefs=response.css('.titletype .son2 .sright a::attr(href)').extract()
        types=response.css('.titletype .son2')
        for scope in types:
            parent_catalog=scope.css('.sleft a::text').extract_first()[:-1]
            meta={'parent_catalog':parent_catalog}
            hrefs=scope.css('.sright a')
            for href in hrefs:
                url=href.css('::attr(href)').extract_first()
                catalog=href.css('::text').extract_first()
                meta['catalog']=catalog
                url=urlparse.urljoin(self.start_urls[0],url)
                request=scrapy.Request(url,callback=self.parse_type)
                request.meta['item']=meta
                yield request


    def parse_type(self, response):
        meta=dict()
        meta.update(response.meta.get('item',{}))
        hrefs=response.css('.sonspic .cont p a:first-child::attr(href)').extract()
        for url in hrefs:
            url=urlparse.urljoin(self.start_urls[0],url)
            req=scrapy.Request(url,callback=self.parse_list)
            req.meta['item']=meta
            yield req
        nextpage=response.css('.pages').xpath('a[last()]')
        if nextpage.xpath('text()').extract_first()==u'下一页':
            page = nextpage.xpath('@href').extract_first()
            url=urlparse.urljoin(self.start_urls[0],page)
            print url
            request=scrapy.Request(url,callback=self.parse_type)
            request.meta['item']=meta
            yield request


    def parse_list(self, response):
        meta=dict()
        meta['book_name']=response.css('.sonspic .cont h1 b::text').extract_first()
        meta['introduce']=response.css('.sonspic .cont p').extract_first()
        meta.update(response.meta['item'])
        lists=response.css('.bookcont')
        for scope in lists:
            hrefs=scope.css('a::attr(href)').extract()
            meta['chapter_name']=scope.css('.bookMl strong::text').extract_first()
            for url in hrefs:
                url=urlparse.urljoin(self.start_urls[0],url)
                req=scrapy.Request(url,callback=self.parse_detail)
                req.meta['item']=meta
                yield req

    def parse_detail(self,response):

        title=response.css('.cont h1 b::text').extract_first()
        author=response.css('.cont .source a::text').extract_first()
        content=response.css('.cont .contson p').extract()
        #content=[]
        info={'title':title,'author':author,'content':''.join(content)}
        info.update(response.meta.get('item',{}))
        page_id=response.css('.cont h1 a[href*="ShowYizhu"]').re_first(r'\d+')
        if page_id is not None:
            yi_url='https://so.gushiwen.org/guwen/ajaxbfanyi.aspx?id='+str(page_id)
            req=scrapy.Request(yi_url,callback=self.parse_yizhu)
            req.meta['item']=info
            yield req
        else:
            yield info
        #yield info

    def parse_yizhu(self,response):
        yizhu=response.css('.shisoncont p').extract()
        info={'yizhu':''.join(yizhu)}
        info.update(response.meta['item'])
        yield info

