# -*- coding: utf-8 -*-

import re
import json
import scrapy

from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ArticleItem


def process_value(value):
    res = None
    match = re.search(r"\d+/\d+/\d+/([^/]+)/", value)
    if match:
        slug = match.group(1)
        res = f"https://techcrunch.com/wp-json/wp/v2/posts?slug={slug}"
    return res


class ArticlesSpider(CrawlSpider):
    name = "articles"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/"]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                process_value=process_value,
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        item = {}
        json_res = json.loads(response.body)

        if len(json_res) >= 1 and isinstance(json_res, list):
            data = json_res[0]
            content = HtmlResponse(
                response.url, body=bytes(data["content"]["rendered"], "utf-8")
            )

            loader = ItemLoader(item=ArticleItem(), response=content)
            loader.add_value("title", data["title"]["rendered"])
            loader.add_value("publish_date", data["date_gmt"])

            loader.add_css("content", "*::text")
            loader.add_css("image_urls", "img::attr(src)")
            loader.add_css("links", "a::attr(href)")

            item = loader.load_item()

        return item
