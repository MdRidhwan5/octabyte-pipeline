import os
import json
import requests
from datetime import datetime

def lambda_handler(event, context):
    # Get your NewsAPI key from environment variables
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        return {
            "statusCode": 500,
            "body": json.dumps("Error: NEWS_API_KEY environment variable not set")
        }

    # Example endpoint to get logistics/supply chain news (adjust query as needed)
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=logistics OR supply chain&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"apiKey={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # You can process/store data here, for now just return the total results and first article title
        total_results = data.get("totalResults", 0)
        first_title = data["articles"][0]["title"] if data["articles"] else "No articles found"

        return {
            "statusCode": 200,
            "body": json.dumps({
                "totalResults": total_results,
                "firstArticleTitle": first_title,
                "fetchedAt": datetime.utcnow().isoformat() + "Z"
            }),
        }

    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Request failed: {str(e)}")
        }