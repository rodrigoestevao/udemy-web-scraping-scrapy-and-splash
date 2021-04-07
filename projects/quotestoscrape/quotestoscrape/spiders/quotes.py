import scrapy

from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ['http://quotes.toscrape.com/js/']

    script = """
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return splash:html()
    end
    """

    def start_requests(self):
        yield SplashRequest(
            url="http://quotes.toscrape.com/js/",
            callback=self.parse,
            args={"wait": 1, "lua_source": self.script},
            endpoint="execute",
        )

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            yield {
                "text": quote.xpath(".//span[@class='text']/text()").get(),
                "author": quote.xpath(
                    ".//span[not(@class)]/small[@class='author']/text()"
                ).get(),
                "tags": quote.xpath(
                    ".//div[@class='tags']/a[@class='tag']/text()"
                ).getall(),
            }

        next_page = response.xpath(
            "//ul[@class='pager']/li[@class='next']/a/@href"
        ).get()

        if next_page:
            absolut_url = response.urljoin(next_page)
            yield SplashRequest(
                url=absolut_url,
                callback=self.parse,
                endpoint="execute",
                args={"wait": 0.5, "lua_source": self.script},
            )
