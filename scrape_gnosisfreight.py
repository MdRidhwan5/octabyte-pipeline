import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
URL = "https://www.gnosisfreight.com"

# Get today's date for file naming
today = datetime.today().strftime("%Y-%m-%d")
output_filename = f"gnosisfreight_{today}.txt"

try:
    # Send GET request
    response = requests.get(URL)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract visible text from main sections
    sections = soup.find_all(["h1", "h2", "p"])
    extracted_text = "\n".join([section.get_text(strip=True) for section in sections])

    # Save to file
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"GnosisFreight content saved to {output_filename}")

except Exception as e:
    print(f"Scraping failed: {e}")
