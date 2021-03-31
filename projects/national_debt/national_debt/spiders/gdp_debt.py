import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//table[@class='jsx-1487038798 table table-striped tp-table-body']/tbody/tr")
        for row in rows:
            country = row.xpath(".//td[1]/a/text()").get()
            debit_ratio = row.xpath(".//td[2]/text()").get()
            yield {
                "country_name": country,
                "gdp_debt": debit_ratio
            }
