from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from news_sources.config import LRU_MAX_ITEMS
import importlib
import time

class NewsSource(object):

    def __init__(self, name):

        self.name = name

    def get_news(self, query=None):
        
        raise NotImplementedError

    def parse_data(self, request_data):

        raise NotImplementedError

class NewsManager(object):

    def __init__(self, news_providers_list):

        self.providers = []

        for provider, provider_path in news_providers_list.items():
            module = importlib.import_module(provider_path)
            provider_class = getattr(module, provider)

            self.providers.append(provider_class()) # Create an instance of the Provider class

    @lru_cache(maxsize=LRU_MAX_ITEMS)
    def fetch_news(self, query=None):

        news    = []
        threads = []
        
        with ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            for news_provider in self.providers:
                threads.append(executor.submit(news_provider.get_news, query))
            
        for task in as_completed(threads):
            news.extend(task.result())

        return news
