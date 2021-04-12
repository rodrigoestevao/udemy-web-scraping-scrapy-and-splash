# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join, Compose


class ArticleItem(Item):
    title = Field(output_processor=TakeFirst())
    publish_date = Field(output_processor=TakeFirst())
    content = Field(
        ouput_processor=Compose(lambda v: filter(None, v), Join(""))
    )
    image_urls = Field()
    links = Field()
