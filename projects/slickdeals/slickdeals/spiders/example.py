import scrapy

from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys

from scrapy_selenium import SeleniumRequest


class ExampleSpider(scrapy.Spider):
    name = "example"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://duckduckgo.com",
            wait_time=3,
            screenshot=True,
            callback=self.parse,
        )

    def parse(self, response):
        # img = response.meta["screenshot"]
        # with open("screenshot.png", "wb") as f:
        #     f.write(img)
        #     f.flush()
        driver = response.meta["driver"]
        search_input = driver.find_element_by_xpath(
            "//input[@id='search_form_input_homepage']"
        )
        search_input.send_keys("My User Agent")
        search_input.send_keys(Keys.ENTER)

        # driver.save_screenshot("after_filling_input.png")

        # NOTE:
        # The response object is related with the first request, retrieved from
        # start_requests(), for this reason we have to convert the driver
        # response to a valid Selector instance.
        response = Selector(text=driver.page_source)

        links = response.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield {"url": link.xpath(".//@href").get()}
