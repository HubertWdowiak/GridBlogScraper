import unittest
from utils import get_last_date, scrap_new_urls
import datetime


class TestUtils(unittest.TestCase):
    def test_get_last_date(self):
        last_date = get_last_date()
        self.assertGreaterEqual(last_date, '2021-03-15')

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


if __name__ == '__main__':
    unittest.main()
