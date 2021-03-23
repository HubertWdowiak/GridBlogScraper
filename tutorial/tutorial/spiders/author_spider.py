import ast

import scrapy
import logging
from ..scrapy_logger_utils import set_scrapy_logger


class AuthorSpider(scrapy.Spider):
    """
     An author scraper for all the available authors in the griddynamics domain.
        For each author, it scraps:
        1) full name,
        2) job title,
        3) url for linkedin profile,
        4) amount of written articles.
    """
    name = "authors"
    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ast.literal_eval(kwargs.pop('start_urls'))
        set_scrapy_logger(logging.WARNING)

    def parse(self, response, **kwargs):
        author = {
            'name': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > h3::text').get(),
            'jobtitle': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > p::text').get(),
            'linkedin': response.css('.modalbg > .linkedin::attr(href)').get(),
            'articles': len(response.css('#woe > div.modalbg > div > div.postsrow > div').getall()) - 1
        }
        logging.info(f"Scraped author: {author['name']}")
        yield author
