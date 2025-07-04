import feedparser
from datetime import datetime

# RSS feed URL for FreightWaves
FEED_URL = "https://www.freightwaves.com/feed"

# Parse RSS
feed = feedparser.parse(FEED_URL)

# Prepare output file
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"freightwaves_{date_str}.txt"

# Write article titles to file
with open(filename, "w", encoding="utf-8") as f:
    for entry in feed.entries:
        f.write(entry.title + "\n")

print(f"Scraped {len(feed.entries)} headlines to {filename}")
