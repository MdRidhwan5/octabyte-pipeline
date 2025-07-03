from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')
filename = f'freightwaves_{today}.txt'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Load the page
    page.goto("https://www.freightwaves.com/news", timeout=60000)
    page.wait_for_timeout(5000)  # wait 5 seconds

    html = page.content()
    browser.close()

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    headlines = []

    for h2 in soup.find_all('h2'):
        title = h2.get_text(strip=True)
        if title:
            headlines.append(title)

    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("📰 Top Headlines from Freightwaves\n")
        f.write(f"Date: {today}\n\n")
        for line in headlines:
            f.write(f"- {line}\n")

    print(f" Headlines saved to file: {filename}")
