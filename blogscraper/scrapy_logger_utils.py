import logging


def set_scrapy_logger(level=logging.WARNING):
    logger_names = ['scrapy.core.scraper',
                    'scrapy.core.engine',
                    'scrapy.middleware',
                    'scrapy.statscollectors',
                    'scrapy.extensions.logstats',
                    'scrapy.extensions.feedexport',
                    'scrapy.extensions.telnet',
                    'scrapy.crawler']

    for name in logger_names:
        scraper = logging.getLogger(name)
        scraper.setLevel(level)