import unittest
import sys, os
import logging


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'etl/ingest/src')))
from ingest_api import ExchangeRateIngest, CoinMarketCapIngest
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class TestExchangeRateIngest(unittest.TestCase):

    def test_api_get(self):
        token = os.getenv('EXCHANGERATE_API_TOKEN')
        ingest = ExchangeRateIngest(token)
        rs = ingest.api_get(currencies='USD,GBP,CAD,JPY,MXN')
        self.assertTrue(rs is not None)
        self.assertTrue(type(rs) == dict)
        self.assertTrue(rs['success'])
        for key in rs['quotes'].keys():
            self.assertTrue(key.startswith('USD'))
        logger.info(rs)

class TestCoinMarketCapIngest(unittest.TestCase):

    def test_api_get(self):
        token = os.getenv('COINMARKETCAP_API_TOKEN')
        ingest = CoinMarketCapIngest(token)
        rs = ingest.api_get(slug='bitcoin,ethereum,solana', convert='USD')
        self.assertTrue(rs is not None)
        self.assertTrue(type(rs) == dict)
        self.assertEqual(rs['status']['error_code'], 0)
        logger.info(rs)

if __name__ == '__main__':
    unittest.main()