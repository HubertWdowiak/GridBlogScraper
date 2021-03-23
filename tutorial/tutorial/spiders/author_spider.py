import ast

import scrapy

from scrapy.utils.log import configure_logging
import logging

class AuthorSpider(scrapy.Spider):
    name = "authors"
    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        x = ast.literal_eval(kwargs.pop('start_urls'))
        self.start_urls = x

    def parse(self, response, **kwargs):
        yield {
            'name': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > h3::text').get(),
            'jobtitle': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > p::text').get(),
            'linkedin': response.css('.modalbg > .linkedin::attr(href)').get(),
            'articles': len(response.css('#woe > div.modalbg > div > div.postsrow > div').getall()) - 1
        }

# class AuthorSpider(scrapy.Spider):
#     name = "authors"
#     start_urls = ['https://blog.griddynamics.com/all-authors/']
#
#     def parse(self, response, **kwargs):
#         if 'all-authors' in response.url:
#             for author_site in response.css('.viewauthor::attr(href)').getall():
#                 yield scrapy.Request(response.urljoin(author_site), callback=self.parse)
#         yield {
#             'name': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > h3::text').get(),
#             'jobtitle': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > p::text').get(),
#             'linkedin': response.css('.modalbg > .linkedin::attr(href)').get(),
#             'articles': len(response.css('#woe > div.modalbg > div > div.postsrow > div').getall()) - 1
#         }

