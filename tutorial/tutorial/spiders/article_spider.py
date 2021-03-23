from datetime import datetime

import scrapy
import ast


class ArticleSpider(scrapy.Spider):
    """
    An article scraper for all the available articles in the griddynamics domain.
        For each article, it scraps:
        1) title,
        2) url to full version,
        3) first 160 symbols of text,
        4) publication date,
        5) authors (full names),
        6) tags.
    """
    name = "articles"

    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        x = ast.literal_eval(kwargs.pop('start_urls'))
        self.start_urls = x

    def parse(self, response, **kwargs):
        if 'author' in response.url:
            yield {
                'name': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > h3').get(),
                'jobtitle': response.css('#woe > div.modalbg > div > div.row > div.titlewrp > p::text').get(),
                'linkedin': response.css('.modalbg > .linkedin::attr(href)').get(),
            }
        else:
            title = response.css('#wrap > h1::text').get()
            url = response.url
            text = "".join(response.css('#woe > section.postbody > div > p::text').getall())[:160]
            date = response.xpath('//*[@id="wrap"]/div/div[2]/text()').extract()[0][:-5].strip()
            date = datetime.strptime(date, '%b %d, %Y')

            raw_authors = response.css('#wrap > div > div.author.authors > div > span > a > span::text').getall()
            raw_authors = [author.strip() for author in raw_authors if author.strip() != ""]
            authors_urls = response.css('.goauthor::attr(href)').getall()

            authors = [(author, url) for author, url in zip(raw_authors, authors_urls)]
            tags = response.css('.post-tags > a::text').getall()

            yield {
                'title': title,
                'url': url,
                'text': text,
                'date': date,
                'authors': authors,
                'tags': tags
            }
