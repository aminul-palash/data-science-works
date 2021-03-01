import scrapy
from ..items import QuotetutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        item = QuotetutorialItem()
        for quote in response.css('div.quote'):
            # yield {
            #     'text': quote.css('span.text::text').get(),
            #     'author': quote.css('small.author::text').get(),
            #     'tags': quote.css('div.tags a.tag::text').getall(),
            # }
            text = quote.css('span.text::text').extract_first(),
            author = quote.css('small.author::text').extract_first(),
            tags = quote.css('div.tags a.tag::text').extract(),
            item['quote'] = text[0].strip()
            item['author'] = author[0].strip()
            item['tags'] = tags[0]

            yield item