import scrapy
from datetime import datetime

class UrlSpider(scrapy.Spider):
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

    def __init__(self, last_date, **kwargs):
        super().__init__(**kwargs)
        self.last_date = datetime.strptime(last_date[:10], '%Y-%m-%d')

    def parse(self, response, **kwargs):

        urls = response.css('.card::attr(href)').getall()
        raw_dates = response.css('.card .author .name::text').getall()
        dates = [" ".join(i.split()[:3]) for i in raw_dates if i.split() != []]

        new_urls = []
        for i in range(len(urls)):
            if datetime.strptime(dates[i], '%b %d, %Y') > self.last_date:
                new_urls.append(urls[i])

        yield {
            response.url: new_urls,
        }
