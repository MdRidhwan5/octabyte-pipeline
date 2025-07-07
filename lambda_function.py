import requests
import os
from datetime import datetime
import json

def lambda_handler(event, context):
    # Read from environment variable
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

    if not NEWS_API_KEY:
        return {
            "statusCode": 500,
            "body": "API key is missing. Set NEWS_API_KEY in Lambda environment variables."
        }

    url = f"https://newsapi.org/v2/everything?q=logistics OR supply chain&language=en&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        filename = f"/tmp/newsapi_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return {
            "statusCode": 200,
            "body": f"Scraped data saved to {filename}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
