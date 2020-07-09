from news_sources import NewsSource
from news_sources.config import REQUEST_TIMEOUT
from news_sources.exceptions import InvalidAPIKey, APIKeyMissing
from .config import API_KEY
from enum import Enum
import requests

class FieldMapper(Enum):
    """
    Maps the News Source's fields to the required fields in o/p
    """

    HEADLINE = 'title'
    LINK     = 'url'

class NewsApi(NewsSource):
    
    BASE_URI = 'https://newsapi.org/v2/everything?'

    def __init__(self, API_KEY=API_KEY):

        if API_KEY is None:
            raise APIKeyMissing(self.__class__.__name__)

        self.API_KEY = API_KEY

    def get_news(self, query=None):

        q_param     = 'general' if query is None else query
        request_url = f'{self.BASE_URI}q={q_param}&apiKey={self.API_KEY}' 

        try:
            req = requests.get(request_url, timeout=REQUEST_TIMEOUT)
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise e

        if req.status_code != 200:
            if req.status_code == 401:
                raise InvalidAPIKey(self.__class__.__name__)
        
        return self.parse_data(req.json())
    
    def parse_data(self, request_data):

        posts    = []
        articles = request_data.get('articles', {})

        for article in articles:
            posts.append({
                'headline' : article.get(FieldMapper.HEADLINE.value),
                'link'     : article.get(FieldMapper.LINK.value),
                'source'   : self.info['label']
            })

        return posts
    
    @property
    def info(self):
        
        return {
            'slug'  : 'newsapi',
            'label' : 'NewsAPI',
            'url'   : 'https://newsapi.org/',
        }
