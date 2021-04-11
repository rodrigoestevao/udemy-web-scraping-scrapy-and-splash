# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MongoPipeline(object):

    collection_name = "computerdeals"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())


class SQLlitePipeline(object):
    def open_spider(self, spider):
        self.connection = sqlite3.connect("slickdeals.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS computer_deals (
            name TEXT,
            link TEXT,
            store TEXT,
            price TEXT
        )
        """
        )

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            """
        INSERT INTO computer_deals (name, link, store, price) VALUES (?,?,?,?)
        """,
            (
                item.get("name"),
                item.get("link"),
                item.get("store"),
                item.get("price"),
            ),
        )
        self.connection.commit()
        return item
