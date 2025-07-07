from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

try:
    url = "https://sell.g2.com"
    driver.get(url)

    wait = WebDriverWait(driver, 15)

    # ✅ Wait for <body> instead of <main>
    body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Extract full text from body
    text_content = body.text

    # Prepare data
    data = {
        "url": url,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": text_content
    }

    # Save to JSON
    filename = f"sell_g2_com_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Content saved to: {filename}")

finally:
    driver.quit()
