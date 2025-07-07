# newsapi_scraper.py
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("NEWSAPI_KEY")

# Define search parameters
query = "logistics OR supply chain"
url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=20&sortBy=publishedAt&apiKey={api_key}"

# Make the request
response = requests.get(url)

if response.status_code == 200:
    news_data = response.json()
    
    # Generate filename with timestamp
    today_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"newsapi_logistics_{today_str}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

    print(f"News data saved to {filename}")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
