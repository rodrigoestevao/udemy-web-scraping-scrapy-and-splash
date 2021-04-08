import scrapy


from shutil import which

from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CoinSpiderSelenium(scrapy.Spider):
    name = "coin_selenium"
    allowed_domains = ["web.archive.org"]
    start_urls = [
        "https://web.archive.org/web/20200116052415if_/https://www.livecoin.net/en/"
    ]  # NOQA

    def __init__(self):
        chrome_path = which("chromedriver")

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options
        )
        driver.set_window_size(1920, 1080)
        driver.get(self.start_urls[0])

        rur_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        rur_tab[4].click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath(
            "//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"  # NOQA
        ):
            yield {
                "currency_pair": currency.xpath(".//div[1]/div/text()").get(),
                "volume_24h": currency.xpath(".//div[2]/span/text()").get(),
            }
