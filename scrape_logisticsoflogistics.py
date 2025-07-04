import requests
from bs4 import BeautifulSoup
import datetime
import json

def scrape_logisticsoflogistics():
    url = 'https://www.thelogisticsoflogistics.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/115.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return
    except Exception as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Inspect the site structure. As of now, blog post titles appear inside <h2 class="entry-title"> tags.
    posts = soup.find_all('h2', class_='entry-title')

    headlines = []

    for post in posts:
        # Extract text from anchor inside the h2 tag
        a_tag = post.find('a')
        if a_tag and a_tag.text.strip():
            headlines.append(a_tag.text.strip())

    # Save to JSON file with today's date
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'thelogisticsoflogistics_{date_str}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(headlines, f, indent=2, ensure_ascii=False)

    print(f"LogisticsofLogistics content saved to {filename}!")

if __name__ == '__main__':
    scrape_logisticsoflogistics()
