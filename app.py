from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv
load_dotenv()
from news_sources import NewsSource, NewsManager
from news_sources.exceptions import InvalidAPIKey, APIKeyMissing
import json

news_providers = {
    'Reddit'  : 'news_sources.reddit',
    'NewsApi' : 'news_sources.news_api'
}
news_manager = NewsManager(news_providers)

app = FastAPI()

@app.get("/", response_class=ORJSONResponse)
async def ping():
    return {"v" : "0.1"}

@app.get("/news", response_class=ORJSONResponse)
async def news(query: str=None):
    
    try:
        return news_manager.fetch_news(query)
    except InvalidAPIKey as e:
        provider = e.provider
        raise HTTPException(status_code=401, detail=f'{provider} : Invalid API key')
    except APIKeyMissing as e:
        provider = e.provider
        raise HTTPException(status_code=401, detail=f'{provider} : API key not provided') 
