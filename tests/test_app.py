from fastapi.testclient import TestClient
from news_aggregator.app import app
import random

client = TestClient(app)

def test_ping():
    """Test Ping API
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()      == {"v" : "0.1"}

def test_news_general():
    """Test the general news API
    """
    response = client.get('/news')

    assert response.status_code == 200
    assert len(response.json()) > 0 # There's always some general news

def test_news_query():
    """Test with query `corona`
    """
    response = client.get('/news?query=corona')

    assert response.status_code == 200
    assert len(response.json()) > 0 # There's gotta be news regarding Corona

def test_fields_in_general_news():
    """Check that the 3 required fields are always present in the o/p (if any)
    """

    response = client.get('/news')

    articles        = response.json()
    num_of_articles = len(articles)
    assert(num_of_articles > 0)

    random_articles = random.sample(articles, num_of_articles//5) # Get 20% of articles for testing

    for article in random_articles:
        assert('headline' in article)
        assert('link' in article)
        assert('source' in article)

def test_fields_in_query_news():
    """Check that the 3 required fields are always present in the o/p (if any)
    """

    response = client.get('/news?query=corona')

    articles        = response.json()
    num_of_articles = len(articles)
    assert(num_of_articles > 0)
    
    random_articles = random.sample(articles, num_of_articles//5) # Get 20% of articles for testing

    for article in random_articles:
        assert('headline' in article)
        assert('link' in article)
        assert('source' in article)

def test_nonsense_query():
    """Check that nonsense queries don't generate news
    """

    response = client.get('/news?query=makesnosense_gibberish')

    assert response.status_code == 200
    assert len(response.json()) == 0 # Nonsense query
