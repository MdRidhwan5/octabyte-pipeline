from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# Target LeadIQ company URL
url = 'https://leadiq.com/c/gnosis-freight/5fcf6529a856d346f831079f'
driver.get(url)
time.sleep(5)  # Allow JavaScript to load

# Extract full rendered HTML
html = driver.page_source
driver.quit()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract company name
company_name_tag = soup.find('h1')
company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

# Extract website URL
website = None
website_tag = soup.find('a', href=True, string=re.compile(r'www|http'))
if website_tag:
    website = website_tag['href']

# Extract location
location = None
location_tag = soup.find('div', string=re.compile(r'Location', re.I))
if location_tag and location_tag.find_next():
    location = location_tag.find_next().get_text(strip=True)

# Extract employee count
employee_count = None
emp_tag = soup.find('div', string=re.compile(r'Employees', re.I))
if emp_tag and emp_tag.find_next():
    employee_count = emp_tag.find_next().get_text(strip=True)

# Extract LinkedIn URL
linkedin_url = None
linkedin_tag = soup.find('a', href=re.compile(r'linkedin\.com/company'))
if linkedin_tag:
    linkedin_url = linkedin_tag['href']

# Extract email format
email_format = None
email_tag = soup.find(string=re.compile(r'@'))
if email_tag:
    match = re.search(r'[a-z]+\.[a-z]+@[a-z]+\.[a-z]+', email_tag)
    if match:
        email_format = match.group()

# Extract insights section and format it with line breaks
insights_section = soup.find('div', {'id': 'insights'})
insights_text = []
if insights_section:
    raw_paragraphs = [p.get_text(strip=True) for p in insights_section.find_all('p') if p.get_text(strip=True)]

    formatted_insights = []
    for para in raw_paragraphs:
        # Try splitting title and content at the first lowercase-to-uppercase or colon
        match = re.match(r'^([^-:\n]+?):?\s*(.*)', para)
        if match:
            title = match.group(1).strip()
            desc = match.group(2).strip()
            formatted = f"- {title}:\n  {desc}"
        else:
            formatted = f"- {para}"
        formatted_insights.append(formatted)

    # Remove duplicates
    insights_text = list(dict.fromkeys(formatted_insights))



# Extract industry tags
tags_section = soup.find_all('span', string=re.compile(r'logistics|supply chain|freight', re.I))
tags = list(set(tag.get_text(strip=True) for tag in tags_section)) if tags_section else []

# Prepare the data dictionary
company_data = {
    'company_name': company_name,
    'source_url': url,
    'website': website,
    'location': location,
    'employee_count': employee_count,
    'linkedin_url': linkedin_url,
    'email_format': email_format,
    'insights': insights_text,
    'industry_tags': tags
}

# Dynamic filename using today's date
today_str = datetime.now().strftime('%Y-%m-%d')
filename = f'leadiq_{today_str}.json'

# Save to JSON file
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(company_data, f, ensure_ascii=False, indent=4)

print(f"Data saved to '{filename}'")
