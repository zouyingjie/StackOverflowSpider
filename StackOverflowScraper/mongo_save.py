# -*- coding: utf-8 -*-import pymongo
from pymongo import MongoClient


class MongoPipeline(object):

    collection_name = 'stack_scrapy_items'

    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.cache
        self.db.stack_scrapy_items.create_index([('title', 'text'), ], )

    # def __init__(self, mongo_uri, mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )

    def open_spider(self, spider):
        pass
        # self.client = MongoClient("localhost", "27017")
        # self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db.stack_scrapy_items.insert(dict(item))
        return item


mongoPipeline = MongoPipeline()