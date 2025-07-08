# 🧩 Adding New Crawlers or APIs to the Pipeline

This guide explains how to extend the data pipeline by adding new website crawlers or integrating new APIs.

---

## 1. Adding a New Website Crawler

1. **Create a new Python script** in the `crawlers/` folder:
```

crawlers/
└── newsource.py

````

2. **Scrape content** using `BeautifulSoup`, `Selenium`, or other tools. The script should:
- Output structured data as a Python `dict` or `list`
- Save the output to a file like `newsource_YYYY-MM-DD.json`

3. **Upload the output** using:
```bash
python upload_to_s3.py newsource_2025-07-08.json newsource
````

---

## 2. Adding a New News API Source

1. **Clone the `lambda_newsapi/` package** as a starting point.

2. Replace `newsapi_scraper.py` with a new API handler script.

3. Update `lambda_function.py` to call the new script and format the data as needed.

4. Zip the updated Lambda folder (including `requests` dependencies) and upload to AWS Lambda.

5. Use EventBridge to schedule it (e.g., every 12 or 24 hours).

---

## 3. (Optional) Automate via Lambda or Airflow

* Add the crawler or API logic to a new AWS Lambda function or Airflow DAG.
* Make sure it:

  * Logs to CloudWatch
  * Handles errors gracefully
  * Stores new data in S3 under the correct path (`/raw/source/YYYY-MM-DD/`)

---

## ✅ Best Practices

* Respect `robots.txt` and terms of service.
* Never commit `.env` or AWS keys.
* Validate that new crawlers don’t duplicate existing entries.