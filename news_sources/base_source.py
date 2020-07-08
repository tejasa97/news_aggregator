from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from news_sources.config import LRU_MAX_ITEMS
import importlib
import time

class NewsSource(object):
    """
    Base Class for all news sources

    Parameters
    ----------
    name : str
        Name of news source
    """
    def __init__(self, name):

        self.name = name

    def get_news(self, query=None):
        """
        Fetches the news by query

        Parameters
        ----------
        query : str
            News search query
        """
        
        raise NotImplementedError

    def parse_data(self, request_data):
        """
        Parses the request response

        Parameters
        ----------
        request_data : json
            HTTP response json

        Returns
        ----------
        news : dict
            Parsed news for the news source
        """

        raise NotImplementedError

class NewsManager(object):

    def __init__(self, news_providers_list):
        """
        Manages all the news sources

        Creates an instance of provided news sources and registers with the News Manager

        Parameters
        ----------
        news_providers_list : dict
            dict containing path and name of news sources Classes
        """

        self.providers = []

        for provider, provider_path in news_providers_list.items():
            module = importlib.import_module(provider_path)
            provider_class = getattr(module, provider)

            self.providers.append(provider_class()) # Create an instance of the Provider class

    @lru_cache(maxsize=LRU_MAX_ITEMS)
    def fetch_news(self, query=None):
        """
        Fetches news

        Fetches from all news sources concurrently, and updates the LRU cache by `query` param

        Parameters
        ----------
        query : str
            news search query

        Returns
        ----------
        news : dict
            aggredated news from all news sources
        """

        news    = []
        threads = []
        
        with ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            for news_provider in self.providers:
                threads.append(executor.submit(news_provider.get_news, query))
            
        for task in as_completed(threads):
            news.extend(task.result())

        return news
