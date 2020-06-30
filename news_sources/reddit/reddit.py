from news_sources import NewsSource
from .config import REQUEST_HEADERS
from enum import Enum
import requests

class FieldMapper(Enum):
    
    HEADLINE = 'title'
    LINK     = 'url_overridden_by_dest'

class Reddit(NewsSource):
    
    BASE_URI = 'https://www.reddit.com/r/news'

    def __init__(self):
        super().__init__('reddit')

    def get_news(self, query=None):

        if query is None:
            request_url = f'{self.BASE_URI}/.json' 
        else:
            request_url = f'{self.BASE_URI}/search.json?restrict_sr=on&q={query}' 

        try:
            req = requests.get(request_url, headers=REQUEST_HEADERS)
        except requests.exceptions.ConnectionError as e:
            raise e

        if req.status_code != 200:
            if req.status_code == 401:
                raise Exception("Not authorized/Invalid API key")
        
        return self.parse_data(req.json())
    
    def parse_data(self, request_data):

        posts = []
        articles = request_data.get('data', {}).get('children')

        for article in articles:
            posts.append({
                'headline' : article.get('data').get(FieldMapper.HEADLINE.value),
                'link'     : article.get('data').get(FieldMapper.LINK.value),
                'source'   : self.name
            })

        return posts
