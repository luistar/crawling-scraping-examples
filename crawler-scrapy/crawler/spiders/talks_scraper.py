from pathlib import Path

import scrapy


class TalksScraper(scrapy.Spider):
    name = "talks_scraper"
    talks_counter = 0

    def start_requests(self):
        urls = [
            "https://luistar.github.io/talks/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.css("article.resource-item"):
            yield {
                'id': self.talks_counter,
                'title': article.css("a.pub-title::text").get(),
                'href': article.css("a.pub-title::attr(href)").extract_first()
            }
            self.talks_counter = self.talks_counter + 1

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
