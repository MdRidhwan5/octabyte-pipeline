# newsapi_fetcher.py

import requests
from datetime import datetime
import json
import os

# Store your NewsAPI key in a .env file
from dotenv import load_dotenv
load_dotenv()

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

params = {
    'q': 'logistics OR supply chain',
    'language': 'en',
    'sortBy': 'publishedAt',
    'pageSize': 10,
    'apiKey': NEWSAPI_KEY
}

response = requests.get('https://newsapi.org/v2/everything', params=params)

if response.status_code == 200:
    articles = response.json().get('articles', [])
    output = {
        'query': params['q'],
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'articles': articles
    }

    filename = f"newsapi_logistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"NewsAPI data saved to {filename}")
else:
    print(f"Request failed with status code {response.status_code}")
