import unittest
import sys, os
import logging


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'etl/transform/src')))

from transform_data import LoadTransformIngestedData
from transform_data import FileStorage

where_is_the_data = os.path.abspath(os.path.join(os.path.dirname("."), 'etl/ingest/test/data'))
sys.path.append(where_is_the_data)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

from transform_data import LoadTransformIngestedData, FileStorage


class TestLoadTransformIngestedData(unittest.TestCase):
    def setUp(self):
        
        self.storage = FileStorage(path=where_is_the_data)
        self.data_paths = {
            'coin_filepath': f'{where_is_the_data}/mock_coinmarketcap_data.json',
            'fiat_filepath': f'{where_is_the_data}/mock_exchange_data.json'
        }
        self.transformer = LoadTransformIngestedData(self.storage, self.data_paths)


    def test_load_transform_save(self):
        file_path = self.transformer.load().transform().save()
        self.assertTrue(os.path.isfile(file_path))

if __name__ == '__main__':
    unittest.main()