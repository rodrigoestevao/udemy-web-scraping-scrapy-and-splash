import scrapy

from scrapy.selector import Selector

from scrapy_selenium import SeleniumRequest


class ComputerdealsSpider(scrapy.Spider):
    name = "computerdeals"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/computer-deals/",
            wait_time=3,
            callback=self.parse,
        )

    def parse(self, response):
        products = response.xpath(
            "//ul[@class='dealTiles categoryGridDeals']/li/div[@class='fpItem  ']/div/div[not(@class)]"  # NOQA
        )
        for product in products:
            item_title = product.xpath(
                ".//div[@class='itemImageAndName']/div[@class='itemImageLink']/a[@class='itemTitle bp-p-dealLink bp-c-link']"  # NOQA
            )
            name = item_title.xpath(".//text()").get()
            link = response.urljoin(item_title.xpath(".//@href").get())

            blueprint = product.xpath(
                ".//div[@class='itemImageAndName']/div[@class='itemImageLink']/span[@class='blueprint']"  # NOQA
            )
            store = (
                blueprint.xpath(
                    ".//a[contains(@class, 'itemStore')]/text()"
                ).get()
                or blueprint.xpath(
                    ".//button[contains(@class, 'itemStore')]/text()"
                ).get()
                or ""
            )

            price = product.xpath(
                "normalize-space(.//div[@class='itemInfoLine']/div[@class='priceLine']/div[@class='itemPrice  wide ']/text())"  # NOQA
            ).get()

            yield {"name": name, "link": link, "store": store, "price": price}

        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            yield SeleniumRequest(
                url=f"https://slickdeals.net{next_page}",
                wait_time=3,
                callback=self.parse,
            )
