from abc import ABC, abstractmethod
import requests
from requests import Session
import json
import time
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Storage(ABC):
    @abstractmethod
    def store(self, data: dict) -> None:
        pass

class FileStorage(Storage):
    def __init__(self, path='/tmp'):
        self.path = path

    def store(self, data: dict, file_name: str) -> None:
        file_path = f'{self.path}/{file_name}'
        with open(file_path, 'w') as f:
            json.dump(data, f)

        return file_path
        

class Ingest(ABC):
    def __init__(self, _token: str, _url: str, _path=None):
        self.url = _url
        self.token = _token
        self.path = _path

    @abstractmethod
    def api_post(self, body: dict) -> dict:
        pass

    @abstractmethod
    def api_get(self, **args) -> dict:
        pass



class ExchangeRateIngest(Ingest):

    def __init__(self, token, url='http://api.exchangerate.host', path='live'):
        super().__init__(token, url, path)

    def api_get(self, **args):
        currencies = args.get('currencies')
        get_url = f'{self.url}/{self.path}?access_key={self.token}'
        if currencies:
            get_url = f'{get_url}&currencies={currencies}'
        return requests.get(get_url).json()

    def api_post(self, body):
        logging.error('Trying to do post; not implemented')
        raise NotImplementedError('Exchange Rate post method not implemented')
    
class CoinMarketCapIngest(Ingest):
    def __init__(self, token, url='https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'):
        super().__init__(token, url)
        self.session = Session()
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.token
        }
        self.session.headers.update(headers) 

    def api_get(self, **args):
        return self.session.get(self.url, params=args).json()

    def api_post(self, body):
        logging.error('Trying to do post; not implemented')
        raise NotImplementedError('Coinbase post method not implemented')
    
class IngestController(object):
    def __init__(self, coin_ingest : Ingest, fiat_ingest : Ingest, storage: Storage):
        self.coin_ingest = coin_ingest
        self.fiat_ingest = fiat_ingest
        self.storage = storage
    
    def process_fiat(self, args: dict):
        logger.info(f'ingest fiat {args}')
        return self.fiat_ingest.api_get(**args)
    
    def process_coin(self, args: dict):
        logger.info(f'ingest coin {args}')
        return self.coin_ingest.api_get(**args)
    
    async def digest_data(self, executor, args: dict) -> tuple:
        loop = asyncio.get_running_loop()
        task_fiat = loop.run_in_executor(executor, self.process_fiat, args)
        task_coin = loop.run_in_executor(executor, self.process_coin, args)

        result_fiat, result_coin = await asyncio.gather(task_fiat, task_coin)

        logger.info('both task completed')
        return result_fiat, result_coin
    
    async def store_data(self, executor, data_fiat, data_coin) -> dict:
        timestr = time.strftime("%Y%m%d_%H%M%S")

        loop = asyncio.get_running_loop()
        task_fiat = loop.run_in_executor(executor, self.storage.store, data_fiat, f'{timestr}_fiat.json')
        task_coin = loop.run_in_executor(executor, self.storage.store, data_coin, f'{timestr}_coin.json')

        fiat_filename, coin_filename = await asyncio.gather(task_fiat, task_coin)
        return {
            'fiat_filepath': fiat_filename,
            'coin_filepath': coin_filename
        }
    
    async def build_pipeline(self, args: dict):
        executor = ThreadPoolExecutor()
        rs_fiat, rs_coin = await self.digest_data(executor, args)

        rs = await self.store_data(executor, rs_fiat, rs_coin)
        logger.info(rs)
        return rs

    def process_ingestion(self, **args):
        return asyncio.run(self.build_pipeline(args))
