import scrapy

from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = "coin"
    allowed_domains = ["web.archive.org"]
    # start_urls = ['https://web.archive.org/web/20200116052415if_/https://www.livecoin.net/en/']  # NOQA

    script = """
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(1))
        rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb "))
        rur_tab[5]:mouse_click()
        assert(splash:wait(1))
        splash:set_viewport_full()
        return splash:html()
    end
    """

    def start_requests(self):
        yield SplashRequest(
            url="https://web.archive.org/web/20200116052415if_/https://www.livecoin.net/en/",  # NOQA
            callback=self.parse,
            endpoint="execute",
            args={"wait": 1, "lua_source": self.script},
        )

    def parse(self, response):
        print(response.body)
