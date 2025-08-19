import unittest
import sys, os
import logging
import json



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'etl/ingest/src')))
from ingest_api import Ingest, IngestController, FileStorage

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class MockIngestCoinMarketCapIngest(Ingest):
    def __init__(self):
        super().__init__('mock token', 'http://mock_url')

    def api_get(self, **args):
        with open('etl/ingest/test/data/mock_coinmarketcap_data.json') as f:
            return json.load(f)

    def api_post(self):
        pass


class MockIngestExchangeRate(Ingest):
    def __init__(self):
        super().__init__('mock token', 'http://mock_url')

    def api_get(self, **args):
        with open('etl/ingest/test/data/mock_exchange_data.json') as f:
            return json.load(f)

    def api_post(self):
        pass

class TestExchangeRateIngest(unittest.TestCase):

    def test_coinmarket_api_get(self):

        mock_ingest = MockIngestCoinMarketCapIngest()
        data = mock_ingest.api_get()
        self.assertTrue(data is not None)

    def test_mock_exchange_api_get(self):

        mock_ingest = MockIngestExchangeRate()
        data = mock_ingest.api_get()
        self.assertTrue(data is not None)

    def test(self):
        storage = FileStorage()
        coin_ingest = MockIngestCoinMarketCapIngest()
        fiat_ingest = MockIngestExchangeRate()
        controller = IngestController(coin_ingest, fiat_ingest, storage)
        rs = controller.process_ingestion()
        self.assertTrue(controller is not None)
        
        self.assertTrue(os.path.isfile(rs['fiat_filepath']))
        self.assertTrue(os.path.isfile(rs['coin_filepath']))

if __name__ == '__main__':
    unittest.main()