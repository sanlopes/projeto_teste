import scrapy
import json
import html
from unidecode import unidecode


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        "https://g1.globo.com/",
    ]

    def parse(self, response):
        for article in response.css("div.feed-post"):
            title = article.css("a.feed-post-link::text").get()
            url = article.css("a.feed-post-link::attr(href)").get()
            author = article.css("span.feed-post-author::text").get()

            # Decodifica caracteres HTML especiais
            title = html.unescape(title) if title else None
            author = html.unescape(author) if author else None

            # Remove caracteres acentuados
            title = unidecode(title) if title else None
            author = unidecode(author) if author else None

            yield {
                "title": title.strip() if title else None,
                "url": url.strip() if url else None,
                "author": author.strip() if author else None,
            }

        # Rastreia o próximo link de página, se houver
        next_page_url = response.css("a.load-more-link::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def closed(self, reason):
        items = list(self.parse_results)
        with open('noticias.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)
