import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Response, Request
from scrapy.linkextractors import LinkExtractor


class FetchDataSpider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:1313/"]

    output_path = "D:\PycharmProjects\web-crawling-scraping\crawler-scrapy\output"
    current_page_counter = 0

    rules = (Rule(LinkExtractor(), callback="save_page", follow=True), )

    def save_page(self, response: Response):
        with open(f"{self.output_path}/{self.current_page_counter}.html", "w+", encoding="utf-8") as file:
            file.write(response.text)
            self.current_page_counter = self.current_page_counter + 1
        pass
