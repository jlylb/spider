# -*- coding: utf-8 -*-

# Define here the models for your scraped items
"""
  Last Modified: 2016/1/22 10:56:48
  Last Modified: 2016/1/22 10:57:05









"""
import scrapy


class GbookItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    images = scrapy.Field()
    title = scrapy.Field()
    pic_num = scrapy.Field()
    href = scrapy.Field()
    detail = scrapy.Field()

class ImageDetail(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    image_urls= scrapy.Field()

class Photo(scrapy.Item):
    photo = scrapy.Field()

class ShiciItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    zhujie = scrapy.Field()
