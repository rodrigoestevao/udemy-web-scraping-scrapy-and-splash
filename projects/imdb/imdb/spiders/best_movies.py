import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]

    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    )

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(deny=r'Items/'), callback='parse_item', follow=True),
        Rule(
            LinkExtractor(
                restrict_xpaths=(
                    "//table[@data-caller-name='chart-top250movie']/tbody/tr/td[@class='titleColumn']/a",  # NOQA
                )
            ),
            callback="parse_item",
            follow=True,
            process_request="set_user_agent",
        ),
        # # Used to set the pagination, but it's no longer valid
        # Rule(
        #     LinkExtractor(
        #         restrict_xpaths=("(//a[@class='lister-page-next next-page'])[1]",)
        #     ),
        #     process_request='set_user_agent',
        # ),
    )

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.imdb.com/chart/top/?ref_=nv_mv_250",
            headers={"User-Agent": self.user_agent},
        )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        # item = {}
        # # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # # item['name'] = response.xpath('//div[@id="name"]').get()
        # # item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        yield {
            "title": response.xpath(
                "normalize-space(//div[@class='title_wrapper']/h1/text())"
            ).get(),
            "year": response.xpath(
                "normalize-space(//span[@id='titleYear']/a/text())"
            ).get(),
            "duration": response.xpath(
                "normalize-space(//div[@class='title_wrapper']/div[@class='subtext']/time/text())"  # NOQA
            ).get(),
            "genre": response.xpath(
                "normalize-space(//div[@class='title_wrapper']/div[@class='subtext']/a[not(@title)]/text())"  # NOQA
            ).get(),
            "release_date": response.xpath(
                # "//div[@class='title_wrapper']/div[@class='subtext']/a[count(@title)>0]/text()"  # NOQA
                # OR
                "normalize-space(//div[@class='title_wrapper']/div[@class='subtext']/a[@title != '']/text())"  # NOQA
            ).get(),
            "rating": response.xpath(
                "normalize-space(//span[@itemprop='ratingValue']/text())"
            ).get(),
            "movie_url": response.url,
            "user-agent": response.request.headers["User-Agent"],
        }
