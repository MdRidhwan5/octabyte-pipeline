import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_headlines():
    url = "https://www.freightwaves.com"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    headlines = soup.find_all('h2')  # You can change this to match correct tag
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f'freightwaves_{today}.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        for h in headlines:
            text = h.get_text(strip=True)
            if text:
                f.write(text + '\n')

    print(f"✅ Scraped headlines saved to {filename}")

if __name__ == "__main__":
    scrape_headlines()
