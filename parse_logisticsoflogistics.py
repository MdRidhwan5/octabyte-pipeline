from bs4 import BeautifulSoup
import json
from datetime import datetime

def parse_logisticsoflogistics():
    filename = 'thelogisticsoflogistics_2025-07-04.txt'  # adjust date if needed
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Step 2: Find the headlines/articles you want
    # (This depends on the website's HTML structure)
    
    # Example: find all <h2> tags (commonly used for article headlines)
    headlines = []
    for h2 in soup.find_all('h2'):
        text = h2.get_text(strip=True)
        if text:
            headlines.append(text)
    
    # You can customize the selector after inspecting the HTML source
    
    # Step 3: Save extracted headlines to JSON
    output_filename = f'processed_logisticsoflogistics_{datetime.today().strftime("%Y-%m-%d")}.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(headlines, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(headlines)} headlines and saved to {output_filename}")

if __name__ == "__main__":
    parse_logisticsoflogistics()
