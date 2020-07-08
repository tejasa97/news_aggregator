from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv
load_dotenv()
from news_sources import NewsSource, NewsManager
from news_sources.exceptions import InvalidAPIKey, APIKeyMissing
from starlette.middleware.cors import CORSMiddleware
import json

# For Dynamic instantiation by the NewsManager
""" This makes it easy to add new News Provider classes to the app,
just create a proper module for it, place it in `news_sources` dir,
and make the entry in the following dict
"""
news_providers = {
    'Reddit'  : 'news_sources.reddit',
    'NewsApi' : 'news_sources.news_api'
}

news_manager = NewsManager(news_providers)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Use ORJSONResponse for faster JSON responses"""
@app.get("/", response_class=ORJSONResponse)
async def ping():
    return {"v" : "0.1"}

@app.get("/news", response_class=ORJSONResponse)
async def news(query: str=None):
    """
    Gets news from all registered news sources

    Parameters
    ---------
    query : str
        news search query

    Returns
    ---------
    JSON response containing news from all sources

    Raises
    ---------
    HTTPException 401 : Exception
        If no API keys are provided wherever necessary or invalid API keys are provided
        
    """

    try:
        return news_manager.fetch_news(query)

    except InvalidAPIKey as e:
        provider = e.provider
        raise HTTPException(status_code=401, detail=f'{provider} : Invalid API key')
    except APIKeyMissing as e:
        provider = e.provider
        raise HTTPException(status_code=401, detail=f'{provider} : API key not provided') 
