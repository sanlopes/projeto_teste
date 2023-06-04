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

            title = html.unescape(title).strip() if title else None
            url = response.urljoin(url) if url else None

            if url:
                yield response.follow(url, callback=self.parse_article, meta={'title': title})

        next_page_url = response.css("a.more-link::attr(href)").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_article(self, response):
        author = response.css("span[itemprop='name']::text").get()
        date = response.css("time::attr(datetime)").get()
        text = response.css("article p::text").getall()

        author = html.unescape(author).strip() if author else None
        date = html.unescape(date).strip() if date else None
        text = ' '.join(html.unescape(p).strip() for p in text if p.strip()) if text else None

        author = unidecode(author) if author else None
        date = unidecode(date) if date else None
        text = unidecode(text) if text else None

        news_item = {
            "title": response.meta['title'],
            "url": response.url,
            "author": author,
            "date": date,
            "text": text,
        }

        yield news_item

    def closed(self, reason):
        items = list(self.parse_article(response=None))
        with open('noticias3.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
