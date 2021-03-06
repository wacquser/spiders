# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class QixinbaoCrawlerPipeline(object):
    collection_name = 'data'

    def __init__(self, mongi_uri, mongo_db):
        self.mongo_uri = mongi_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongi_uri= crawler.settings.get('MONGO_URI'),
            mongo_db= crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, 27017)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        self.collection.insert(dict(item))
        return item

