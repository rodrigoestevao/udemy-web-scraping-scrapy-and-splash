import re
import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
products = response.xpath("//div[@id='product-lists']")

key_pattern = re.compile(r"(p-tab-\d+)")
for product in products:
    # Handle the images
    repo = {}
    images = product.xpath(".//div/div[@class='product-img-outer']")
    for image in images:
        image_link = image.xpath(".//a/@href").get()
        image_key = key_pattern.search(
            image.xpath(".//a/@class").get()
        ).group()

    # Handle the titles and prices
    titles = product.xpath(
        ".//div/div[@class='p-title-block']/div[@class='mt-3']"
    )

            # p_title_block = product.xpath(".//div/div[@class='p-title-block']/div[@class='mt-3']")
            # p_title = p_title_block.xpath(".//div/div/div[@class='p-title']").getall()
            # for selector in p_title:
            #     print({
            #         'product_url': None,
            #         'product_image_link': None,
            #         'product_name': None,
            #         'product_price': None
            #     })

