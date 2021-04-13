import math
import json
import scrapy
import logging

from scrapy.exceptions import CloseSpider


class EbooksSpider(scrapy.Spider):
    name = "ebooks"
    allowed_domains = ["openlibrary.org"]

    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    )

    limit = 1000

    def start_requests(self):
        self.offset = 0
        yield scrapy.Request(
            url=f"https://openlibrary.org/subjects/picture_books.json?limit={self.limit}",  # NOQA
            headers={"User-Agent": self.user_agent},
            callback=self.parse,
        )

    def parse(self, response):
        if response.status >= 300:
            logging.error(f"HTTP error code: {response.status}")
            raise CloseSpider()

        data = json.loads(response.body)
        works = data["works"]
        work_count = int(data.get("work_count", "0"))

        for work in works:
            yield {
                "title": work.get("title"),
                "subject": work.get("subject"),
            }

        if work_count >= self.offset:
            self.offset += self.limit

            yield scrapy.Request(
                url=f"https://openlibrary.org/subjects/picture_books.json?limit={self.limit}&offset={self.offset}",  # NOQA
                headers={"User-Agent": self.user_agent},
                callback=self.parse,
            )
