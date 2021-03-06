# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter


class ImdbPipeline:
    def open_spider(self, spider):
        logging.warning("SPIDER OPENED FROM PIPELINE")

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        logging.warning("SPIDER CLOSED FROM PIPELINE")
