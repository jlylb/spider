# -*- coding: utf-8 -*-
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
  Last Modified: 2016/1/15 17:29:37








"""
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import json
import codecs

class GbookPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.jl', 'wb',encoding='utf-8')

    def process_item(self, item, spider):
        #line = json.dumps(dict(item)) + "\n"
        #self.file.write(line)
        json.dump(item,self.file,ensure_ascii=False)
        return item

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('logo.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info): #下载图片
        if item.get('detail',None):
            for detail in item['detail']:
                if detail['image_urls']:
                    for image_url in detail['image_urls']:
                        yield Request(image_url,meta={'item':detail,'name':item['title']})
        if item.get('image_urls',None):
            for image_url in item['image_urls']:
                yield Request(image_url,meta={'item':item,'name':item['title']})


    def file_path(self,request,response=None,info=None):
        item=request.meta['item']
        name=''.join(request.meta['name'])
        sub_name = ''.join(item['name'])

        image_guid = request.url.split('/')[-1]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        filename = u'full/{0}/{1}/{2}'.format(name,sub_name, image_guid)
        return filename
