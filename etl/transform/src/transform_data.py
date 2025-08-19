
import logging
import os, sys
from abc import ABC, abstractmethod
import json
from time import localtime, strftime
from decimal import Decimal
import time
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Storage(ABC):
    @abstractmethod
    def load(self, path: str) -> dict:
        pass

class FileStorage(Storage):
    def __init__(self, path='/tmp'):
        self.path = path

    def load(self, file_path: str) -> dict:
        with open(file_path, 'r') as f:
            return json.load(f)


class LoadTransformData(ABC):

    def __init__(self, storage: Storage):
        self.storage = storage

    @abstractmethod
    def load(self) -> 'LoadTransformData':
        pass

    @abstractmethod
    def transform(self) -> 'LoadTransformData':
        pass

    @abstractmethod
    def save(self) -> None:
        pass

class LoadTransformIngestedData(LoadTransformData):
    def __init__(self, storage: Storage, data_paths: dict):
        super().__init__(storage)
        self.data_paths = data_paths
        self.coin_schema = {
            'id': 'int64',
            'name': 'object',
            'symbol': 'object',
            'slug': 'object',
            'num_market_pairs': 'int64',
            'date_added': 'object',
            'price': 'float64',
            'fiat': 'object',
            'market_cap': 'float64',
            'volume_24h': 'float64',
            'volume_change_24h': 'float64',
            'percent_change_1h': 'float64',
            'percent_change_24h': 'float64',
            'percent_change_7d': 'float64',
            "percent_change_30d": 'float64',
            "percent_change_60d": 'float64',
            "percent_change_90d": 'float64',
            "market_cap": 'float64',
            "market_cap_dominance": 'float64',
            "fully_diluted_market_cap": 'float64',
            "tvl": 'float64',
            'tags': 'int64',
            "max_supply": 'float64',
            "circulating_supply": 'int64',
            "total_supply": 'int64',
            "is_active": 'bool',
            "infinite_supply": 'bool',
            "platform": 'object',
            "cmc_rank": 'int64',
            "is_fiat": 'bool',
            "self_reported_circulating_supply": 'object',
            "self_reported_market_cap": 'object',
            "tvl_ratio": 'float64',
            "last_updated": 'object',
        }
    
    def load(self) -> LoadTransformData:
        ''' Load the data from the storage.
        This method will load the data from the storage and store it in self.coin_data and self.fiat_data
        '''
        if not hasattr(self, 'data_paths'):
            raise ValueError("Data paths not set. Please provide data paths in the constructor.")      
        coin_filepath = self.data_paths['coin_filepath']
        fiat_filepath = self.data_paths['fiat_filepath']
        self.coin_data = self.storage.load(coin_filepath)
        self.fiat_data = self.storage.load(fiat_filepath)
        return self

    def transform(self) -> LoadTransformData:
        ''' Transform the loaded data into a pandas DataFrame.
        This method assumes that self.coin_data and self.fiat_data are already loaded.
        It will flatten the coin data and add fiat data to it'
        '''
        if not hasattr(self, 'coin_data') or not hasattr(self, 'fiat_data'):
            raise ValueError("Data not loaded. Please call load() method first.")   

        assert self.coin_data is not None, "Coin data is not loaded"
        assert self.fiat_data is not None, "Fiat data is not loaded"
        flat_data = self._flattern(self.coin_data, self.coin_schema)
        df = pd.DataFrame(flat_data, columns=self.coin_schema.keys()).astype(self.coin_schema)
        self.prep_fiat_data = self._flattern_fiat_data(self.fiat_data)
        self.df = df.apply(lambda x: self.add_fiat_data(x), axis=1)
        return self
    
    def save(self, path: str = '/tmp') -> None:
        ''' Save the transformed data to a file.
        This method will save the transformed data to a file in PARQUET format.
        '''
        if not hasattr(self, 'df'):
            raise ValueError("Data not transformed. Please call transform() method first.")
        
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_path = f'{path}/{timestr}_transformed_data.parquet'

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        self.df.to_parquet(file_path, index=False)      
        logger.info(f'Transformed data saved to {file_path}')
        return file_path  
       

    def _flattern(self, data: dict, schema: dict) -> dict:
        '''
        Flattern the data to a more usable format.
        param data: dict
        param schema: dict
        return: dict'''

        flat_data = []

        for key, obj in data['data'].items():
            flat_coin_data = {}
            for k in obj.keys():
                if k not in schema.keys():
                    
                    if k == 'quote':
                        for quote in obj[k].keys():
                            flat_coin_data['fiat'] = quote
                        for quote in obj[k].values():
                            for qk in quote.keys():
                                if qk in schema.keys():
                                    flat_coin_data[qk] = quote[qk]
                else:
                    if k == 'tags':
                        flat_coin_data[k] = len(obj[k])
                    else:
                        flat_coin_data[k] = data['data'][key][k]
            flat_data.append(flat_coin_data)
            return flat_data
    
    def _flattern_fiat_data(self, fiat_data: dict) -> dict:
        '''
        Flattern fiat data to a more usable format.
        param fiat_data: dict
        return: dict
        '''
        flat_fiat_data = {}
        if fiat_data['success']:
            source = fiat_data['source']
            per_fiat_data = {}
            per_fiat_data['timestamp'] = strftime('%Y-%m-%d %H:%M:%S', localtime(fiat_data['timestamp']))
            per_fiat_data['source'] = source
            for key, value in fiat_data['quotes'].items():
                per_fiat_data[key[len(source):]] = value
            flat_fiat_data[source] = per_fiat_data

        return flat_fiat_data

    def add_fiat_data(self, row):
        source = row['fiat']
        price = row['price']
        fiat_data = self.prep_fiat_data.get(source, {})
        if fiat_data:
            row['fiat_timestamp'] = fiat_data.get('timestamp', '')
            for key, value in fiat_data.items():
                if key != 'timestamp' and key != 'source':
                    row[key] = Decimal(price * value if isinstance(value, (int, float)) else value)
        return row
