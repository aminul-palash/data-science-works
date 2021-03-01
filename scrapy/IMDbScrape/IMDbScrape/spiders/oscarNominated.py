# 

import scrapy
from ..items import ImdbscrapeItem
# from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser

class IMDbScrapeSpider(scrapy.Spider):
    name = "oscarNominee"
    start_urls = [
        'https://www.imdb.com/list/ls057163321/?start=1&view=detail&sort=list_order,asc&st_dt=&mode=detail&page=1'
    ]
    page_number = 2

    def parse(self, response):

        item = ImdbscrapeItem()
        for data in response.css('.lister-item-content'):

            
            title  =  data.css('.lister-item-header a::text').extract_first(),
            year   =  data.css('.text-muted.unbold::text').extract_first(),
            rating =  data.css('.ipl-rating-star.small .ipl-rating-star__rating::text').extract_first(),
            gross  =  data.css('.ghost~ .text-muted+ span::text').extract_first(),
            intro  = data.css('.ratings-metascore+ p::text , .ipl-rating-widget+ p::text').extract_first()
            
            item['title'] = title[0]
            item['year'] = year[0]
            item['rating'] = rating[0]
            item['gross'] = gross[0]
            item['intro'] = intro.strip()

            yield item
        next_page = 'https://www.imdb.com/list/ls057163321/?start=1&view=detail&sort=list_order,asc&st_dt=&mode=detail&page={}'.format(
            IMDbScrapeSpider.page_number)
        
        if IMDbScrapeSpider.page_number < 5:
            IMDbScrapeSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse, meta={'crawl_once': True})

