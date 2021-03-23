import scrapy
from datetime import datetime
import logging
from ..scrapy_logger_utils import set_scrapy_logger


class UrlSpider(scrapy.Spider):
    """
    An url scraper for all the available articles in the griddynamics domain.
    """
    name = "urls"
    start_urls = [
        'https://blog.griddynamics.com/digital-transformation/',
        'https://blog.griddynamics.com/data-science-ai/',
        'https://blog.griddynamics.com/cloud-and-devops/',
        'https://blog.griddynamics.com/search/',
        'https://blog.griddynamics.com/quality-assurance/',
        'https://blog.griddynamics.com/big-data/',
        'https://blog.griddynamics.com/ui-and-mobile/',
        'https://blog.griddynamics.com/omnichannel-commerce/'
    ]

    def __init__(self, last_date="2020-12-12", **kwargs):
        super().__init__(**kwargs)
        self.last_date = datetime.strptime(last_date[:10], '%Y-%m-%d')
        set_scrapy_logger(logging.WARNING)

    def parse(self, response, **kwargs):
        urls = response.css('.card::attr(href)').getall()
        raw_dates = response.css('.card .author .name::text').getall()
        dates = [" ".join(i.split()[:3]) for i in raw_dates if i.split() != []]

        new_urls = []
        for i in range(len(urls)):
            if datetime.strptime(dates[i], '%b %d, %Y') > self.last_date:
                new_urls.append(urls[i])

        if new_urls:
            logging.info(f'Scraped {len(new_urls)} URLs from {response.url}')
        else:
            logging.info(f'No new blog posts from {response.url}')

        yield {
            response.url: new_urls,
        }
