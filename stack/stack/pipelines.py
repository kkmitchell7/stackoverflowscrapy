# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy import settings
#from scrapy import log
from scrapy.exceptions import DropItem

class MongoDBPipeline(object):

    def __init__(self, mongserver, mongport, mongdb, mongcoll):
        connection = pymongo.MongoClient(
            mongserver,
            mongport
        )
        db = connection[mongdb]
        self.collection = db[mongcoll]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        mongserver = settings.get('MONGODB_SERVER')
        mongport = settings.get('MONGODB_PORT')
        mongdb = settings.get('MONGODB_DB')
        mongcoll = settings.get('MONGODB_COLLECTION')
        return cls(mongserver, mongport, mongdb, mongcoll)

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            #log.msg("Question added to MongoDB database!",
            #        level=log.DEBUG, spider=spider)
        return item


#class StackPipeline:
#    def process_item(self, item, spider):
#        return item
