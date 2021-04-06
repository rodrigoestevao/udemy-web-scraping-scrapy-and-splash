import scrapy
import logging

logger = logging.getLogger(__name__)


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # Different ways to fix the URL issue

            # absulute_url = f"https://{self.allowed_domains[0]}{link}"
            # absulute_url = response.urljoin(link)
            # yield scrapy.Request(url=absulute_url)

            # The meta defined here will be used later by the callback
            yield response.follow(
                url=link,
                callback=self.parse_countries,
                meta={"country_name": name}
            )

        # yield response.follow(
        #     url="https://www.worldometers.info/world-population/china-population/",
        #     callback=self.parse_countries,
        #     meta={"country_name": "China"}
        # )

    def parse_countries(self, response):
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            name = response.request.meta["country_name"]
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                "country_name": name,
                "year": year,
                "population": population,
            }
