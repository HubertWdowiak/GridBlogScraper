import unittest
from utils import get_last_date, scrap_new_urls, scrap_articles_from_urls, update_articles, get_urls_of_new_authors
import datetime
from unittest import mock

mocked_articles = [
    {"title": "A rapid response to COVID-19 \nsupply chain and market shocks: Emerge from the crisis stronger",
     "url": "https://blog.griddynamics.com/rapid-response-to-covid-19-supply-chain-and-market-shocks/",
     "text": "The COVID-19 crisis is clearly the biggest economic disruption the world has seen in the 21st century. "
             "This disruption impacts virtually all industries and all ",
     "date": "2020-04-06 00:00:00",
     "authors": [["Ilya Katsov", "/author/ilya-katsov/"], ["Max Martynov", "/author/max-martynov/"]], "tags": []},
    {"title": "ATG\u2019s black box blocking your e-commerce view? Replatform with microservices",
     "url": "https://blog.griddynamics.com/atgs-black-box-blocking-your-e-commerce-view/",
     "text": "If you want your customers to have a seamless shopping experience no matter where they are or what device"
             " they\u2019re using, but you\u2019re stuck with a black box legac",
     "date": "2020-01-16 00:00:00",
     "authors": [["Max Martynov", "/author/max-martynov/"], ["Ezra Berger", "/author/ezraberger/"]],
     "tags": ["E-commerce"]},
]

mocked_articles_2 = [{"title": "Predictive analytics for promotion and price optimization",
                      "url": "https://blog.griddynamics.com/predictive-analytics-for-promotion-and-price-optimization/",
                      "text": "Pricing decisions are critically important for any business, as pricing is directly "
                              "linked to consumer demand and company profits. Even a slightly suboptimal de",
                      "date": "2018-08-07 00:00:00",
                      "authors": [["Ilya Katsov", "/author/ilya-katsov/"], ["Alex Rodin", "/author/alex-rodin/"]],
                      "tags": ["Machine Learning and Artificial Intelligence", "Data Science"]}]

mocked_authors = [{"name": "Max Martynov", "jobtitle": "CTO", "linkedin": None, "articles": 15},
                  {"name": "Ilya Katsov", "jobtitle": "Head of Practice, Industrial AI", "linkedin": None,
                   "articles": 15}]
mocked_authors_2 = [{"name": "Igor Kononov", "jobtitle": None, "linkedin": None, "articles": 2}]


class TestUtils(unittest.TestCase):

    @mock.patch('utils.read_json_from_file', return_value=mocked_articles)
    def test_get_last_date(self, _):
        last_date = get_last_date()
        self.assertEqual(last_date, '2020-04-06 00:00:00')

        now = str(datetime.datetime.now())
        self.assertGreaterEqual(now, last_date)

    def test_scrap_new_urls(self):
        new_urls = scrap_new_urls('2000-01-01')
        self.assertIn('http://blog.griddynamics.com/rapid-response-to-covid-19-supply-chain-and-market-shocks/',
                      new_urls)
        self.assertIn('http://blog.griddynamics.com/predictive-analytics-for-promotion-and-price-optimization/',
                      new_urls)

        new_urls = scrap_new_urls('2021-01-01')
        self.assertNotIn('http://blog.griddynamics.com/predictive-analytics-for-promotion-and-price-optimization/',
                         new_urls)
        self.assertIn('http://blog.griddynamics.com/deploy-analytical-data-platform-on-aws-in-one-day/',
                      new_urls)

    def test_scrap_articles_from_urls(self):
        urls = ['http://blog.griddynamics.com/rapid-response-to-covid-19-supply-chain-and-market-shocks/']
        data = scrap_articles_from_urls(urls)
        self.assertEqual(len(data), 1)
        self.assertIn('A rapid response to COVID-19', data[0]['title'])
        self.assertEqual('https://blog.griddynamics.com/rapid-response-to-covid-19-supply-chain-and-market-shocks/',
                         data[0]['url'])
        self.assertIn('crisis is clearly the biggest economic disruption', data[0]['text'])
        self.assertEqual("2020-04-06 00:00:00", data[0]['date'])
        self.assertEqual([["Ilya Katsov", "/author/ilya-katsov/"], ["Max Martynov", "/author/max-martynov/"]],
                         data[0]['authors'])
        self.assertEqual([], data[0]['tags'])

    @mock.patch('utils.read_json_from_file', return_value=mocked_articles)
    @mock.patch('utils.save_json_to_file', return_value=None)
    def test_update_articles(self, _, __):
        self.assertEqual(len(update_articles(mocked_articles_2)), len(mocked_articles) + len(mocked_articles_2))

    @mock.patch('utils.read_json_from_file', return_value=mocked_authors)
    def test_get_urls_of_new_authors(self, _):
        new_authors = get_urls_of_new_authors(mocked_articles)
        self.assertEqual(new_authors, ['https://blog.griddynamics.com/author/ezraberger/'])


if __name__ == '__main__':
    unittest.main()
