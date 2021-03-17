from datetime import datetime

import scrapy
import ast


class ArticleSpider(scrapy.Spider):
    name = "articles"

    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        x = ast.literal_eval(kwargs.pop('start_urls'))
        self.start_urls = x

    def parse(self, response, **kwargs):
        title = response.css('#wrap > h1::text').get()
        url = self.start_urls[0]
        text = "".join(response.css('#woe > section.postbody > div > p::text').getall())[:160]
        date = response.xpath('//*[@id="wrap"]/div/div[2]/text()').extract()[0][:-5].strip()
        date = datetime.strptime(date, '%b %d, %Y')

        raw_authors = response.css('#wrap > div > div.author.authors > div > span > a > span::text').getall()
        authors = [author.strip() for author in raw_authors if author.strip() != ""]
        tags = response.css('.post-tags > a::text').getall()

        yield {
            'title': title,
            'url': url,
            'text': text,
            'date': date,
            'authors': authors,
            'tags': tags
        }