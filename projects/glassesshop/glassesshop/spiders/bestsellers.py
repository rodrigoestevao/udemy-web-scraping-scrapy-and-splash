import re
import scrapy

from collections import defaultdict, OrderedDict


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        products = response.xpath("//div[@id='product-lists']")
        prod_key_pattern = re.compile(r"(p-tab-\d+)")

        prod_info = defaultdict(OrderedDict)

        for product in products:
            # Handle the titles and prices
            titles_and_prices = product.xpath(
                ".//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']"
                "/div[@class='p-title-block']/div[@class='mt-3']/div/div"
            )

            # Handle titles
            titles = titles_and_prices.xpath(".//div[@class='p-title']/a")
            for title in titles:
                title_class = title.xpath(".//@class").get()
                prod_key = prod_key_pattern.search(title_class).group()
                product_url = title.xpath(".//@href").get()
                prod_info[prod_key]["product_url"] = product_url
                product_name = title.xpath(".//@title").get()
                prod_info[prod_key]["product_name"] = product_name

            # Handle prices
            prices = titles_and_prices.xpath(".//div[@class='p-price']/div")
            for price in prices:
                price_class = price.xpath(".//@class").get()
                prod_key = prod_key_pattern.search(price_class).group()
                product_price = price.xpath(".//span/text()").get()
                prod_info[prod_key]["product_price"] = product_price

            # Handle the images
            images = product.xpath(".//div/div[@class='product-img-outer']/a")
            for image in images:
                image_class = image.xpath(".//@class").get()
                prod_key = prod_key_pattern.search(image_class).group()
                prod_image_link = image.xpath(
                    ".//img[@class='lazy d-block w-100 product-img-default']/@data-src"
                ).get()
                prod_info[prod_key]["product_image_link"] = prod_image_link

            # Iterate over a copy to allow the cleanup after the iteration
            for prod_key in sorted(prod_info.keys()):
                yield prod_info[prod_key]
                del prod_info[prod_key]
