import scrapy
import json
import html
from unidecode import unidecode


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        "https://www.bbc.com/",
    ]

    def parse(self, response):
        for article in response.css("div.media"):
            title = article.css("a.media__link::text").get()
            url = article.css("a.media__link::attr(href)").get()
            author = article.css("span.media__author::text").get()

            title = html.unescape(title).strip() if title else None
            author = html.unescape(author).strip() if author else None

            title = unidecode(title) if title else None
            author = unidecode(author) if author else None

            news_item = {
                "title": title,
                "url": url.strip() if url else None,
                "author": author,
            }

            yield news_item

        next_page_url = response.css("a.more-link::attr(href)").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def closed(self, reason):
        items = list(self.parse(response=None))
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
