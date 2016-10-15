# -*- coding: utf-8 -*-
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
  Last Modified: 2016/1/15 17:29:37








"""
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
