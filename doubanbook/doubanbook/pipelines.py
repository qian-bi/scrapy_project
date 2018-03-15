# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
from collections import OrderedDict
import json
import cx_Oracle


# class DoubanbookPipeline(object):
#     def process_item(self, item, spider):
#         return item


class JsonWithEncodingPipeline:

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class OraclePipeline:

    def __init__(self):
        dsn = cx_Oracle.makedsn(host='10.101.37.70', port=1521, sid='orcl')
        self.conn = cx_Oracle.connect(user='scrapy', password='scrapy', dsn=dsn)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        self.cur.prepare("INSERT INTO DOUBANSUBJECTITEM(TITLE, URL, CONTENT_INTRO) VALUES (:title, :url, :content_intro)")
        self.cur.executemany(None, item)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
