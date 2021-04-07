import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    )

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//section/div/ol/li/article"),
            callback="parse_item",
            follow=True,
            process_request="set_user_agent",
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths="//ul[@class='pager']/li[@class='next']/a"
            ),
            process_request="set_user_agent",
        ),
    )

    def start_requests(self):
        yield scrapy.Request(
            url="http://books.toscrape.com/",
            headers={"User-Agent": self.user_agent},
        )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        book_name = response.xpath("normalize-space(.//h3/a/@title)").get()
        if book_name:
            price = response.xpath(
                "normalize-space(.//div[@class='product_price']/p[@class='price_color']/text())"  # NOQA
            ).get()

            yield {
                "book_name": book_name,
                "price": price,
            }

        else:
            yield from ()
