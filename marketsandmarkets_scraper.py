# marketsandmarkets_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# Target URL
url = "https://www.marketsandmarkets.com/Market-Reports/supply-chain-management-market-190997554.html"

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)
driver.get(url)

# Wait for JS to load
driver.implicitly_wait(5)
html = driver.page_source
driver.quit()

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract title
title = soup.title.get_text(strip=True) if soup.title else None

# Meta description
description_tag = soup.find("meta", attrs={"name": "description"})
description = description_tag["content"] if description_tag else None

# Extract visible sections
main_content = []
for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
    text = tag.get_text(strip=True)
    if text and len(text.split()) > 4 and not re.match(r'^\s*MarketsandMarkets.*', text):
        main_content.append(text)

# Prepare final data
data = {
    "url": url,
    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "title": title,
    "meta_description": description,
    "content_preview": main_content[:20],  # Show only first 20 content blocks
}

# Save to JSON
filename = f"marketsandmarkets_supplychain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Data saved to: {filename}")
