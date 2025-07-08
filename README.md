# Octa Byte AI – Logistics & Supply‑Chain Data Pipeline

**Author:** Md Ridhwan  
**Stack:** Python 3 · BeautifulSoup · Selenium · boto3 · NewsAPI · AWS Lambda · S3 · CloudWatch  

---

## 1. Project Goal

> Crawl six target logistics/supply‑chain web sources + a free news API, push raw + processed JSON to S3, and run the job automatically every day.

---

## 2. High-Level Flow

```text
┌──────────────────┐     ┌────────────────────┐     ┌────────────┐
│  Python Crawlers │ ─→ │  Raw JSON in S3     │ ─→ │  (Option)  │
└──────────────────┘     └────────────────────┘     │    ETL     │
        ↓                                               ↓
   AWS Lambda + EventBridge (scheduled)         CloudWatch Logs & Alarms (Errors ≥ 1)
````

---

## 3. Repo Layout

```text
.
├─ crawlers/                    # One script per site
│  ├─ gnosis.py
│  ├─ logistics_of_logistics.py
│  └─ ...
├─ lambda_newsapi/             # Self-contained NewsAPI Lambda package
│  ├─ lambda_function.py
│  └─ requests/                # Vendored dependencies
├─ upload_to_s3.py             # Helper for local development
├─ requirements.txt
└─ docs/
   ├─ architecture.png         # Exported from diagrams.net
   └─ sample_outputs/
```

---

## 4. S3 Bucket Convention

```
s3://octabyte-data-pipeline/
└── raw/
    ├── gnosisfreight/
    │   └── 2025-07-07/gnosis_2025-07-07.json
    ├── thelogisticsoflogistics/
    └── ...
```

Each job writes to `raw/<source>/<YYYY-MM-DD>/`
Future processed data can be saved under a `processed/` prefix.

---

## 5. Running Locally

```bash
# Setup virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run one crawler and upload result
python crawlers/gnosis.py
python upload_to_s3.py gnosis_2025-07-07.json gnosisfreight
```

🔐 Secrets are stored in a local `.env` file — this file is **never committed** to GitHub.

---

## 6. Automation on AWS

| Component                    | Purpose                                                         |
| ---------------------------- | --------------------------------------------------------------- |
| **Lambda `newsapi_crawler`** | Fetches news; zipped with `requests` inside                     |
| **EventBridge Rule**         | Triggers Lambda daily at 03:00 UTC                              |
| **IAM Role**                 | Minimal permissions: `s3:PutObject`, `logs:CreateLogGroup`, etc |
| **CloudWatch Alarm**         | Sends alert via email/SNS if `Errors ≥ 1`                       |

---

## 7. Extending – Add a New Site in Under 3 Minutes

1. Add a new script inside `crawlers/` (e.g., `newsite.py`).
2. Make the script return data as a dict/list and save it as `YYYY-MM-DD.json`.
3. Run:
python upload_to_s3.py newfile.json newsource
4. (Optional) Add the script to a Lambda function or Airflow DAG.

---

## 8. Future Improvements & Roadmap

These features are suggested for future development:

* ⏱ Parallel crawling via `Scrapy`, `asyncio`, or `ThreadPoolExecutor`.
* 🔍 Text deduplication and keyword/keyphrase extraction using spaCy or KeyBERT.
* 🐳 Dockerized deployment using ECS Fargate or EKS.
* 📊 Athena/QuickSight integration for dashboards and queryable logs.

---

© 2025 Octa Byte AI. Internal use only.