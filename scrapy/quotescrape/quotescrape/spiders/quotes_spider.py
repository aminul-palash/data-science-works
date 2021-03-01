import scrapy
from ..items import QuotetutorialItem
from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        # csrf_token = response.xpath(
        #     '//input[@name="csrf_token"]').css('input::attr(value)').extract_first()
        csrf_token = response.css('form input::attr(value)').extract_first()
 
        return FormRequest.from_response(response, formdata={
            'csrf_token': csrf_token,
            'username': 'admin@gmail.com',
            'password': 'admin'
        }, callback=self.scrape_item)

    def scrape_item(self, response):
        # open_in_browser(response)
        item = QuotetutorialItem()
        for quote in response.css('div.quote'):
            # yield {
            #     'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
            #     'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
            #     'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            # }
            text = quote.css('span.text::text').extract_first(),
            author = quote.css('small.author::text').extract_first(),
            tags = quote.css('div.tags a.tag::text').extract(),
            item['quote'] = text[0].strip()
            item['author'] = author[0].strip()
            item['tags'] = tags[0]

            yield item

        next_page = response.css('.next a::attr(href)').get()
        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)




# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/page/1/',
#         'http://quotes.toscrape.com/page/2/',
#     ]

#     def parse(self, response):
#         item = QuotetutorialItem()
#         for quote in response.css('div.quote'):
#             # yield {
#             #     'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
#             #     'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
#             #     'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
#             # }
#             text = quote.css('span.text::text').extract_first(),
#             author = quote.css('small.author::text').extract_first(),
#             tags = quote.css('div.tags a.tag::text').extract(),
#             item['quote'] = text[0].strip()
#             item['author'] = author[0].strip()
#             item['tags'] = tags[0]

#             yield item

#         next_page = response.css('.next a::attr(href)').get()
#         # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)