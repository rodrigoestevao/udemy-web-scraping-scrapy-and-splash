import json
import scrapy


class QuotesApiSpider(scrapy.Spider):
    name = "quotes_api"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        data = json.loads(response.body)
        quotes = data.get("quotes")
        for quote in quotes:
            yield {
                "author": quote["author"]["name"],
                "tags": quote.get("tags", []),
                "quote_text": quote.get("text", ""),
            }

        has_next = data.get("has_next")
        if has_next:
            next_page = data.get("page") + 1
            yield scrapy.Request(
                url=f"http://quotes.toscrape.com/api/quotes?page={next_page}"
            )
