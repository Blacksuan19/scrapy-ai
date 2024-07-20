import scrapy


class GenericSpider(scrapy.Spider):
    name = "generic"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/"]

    def parse(self, response):
        pass
