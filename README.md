# Octa Byte AI – Logistics & Supply‑Chain Data Pipeline

**Author:** Md Ridhwan  
**Stack:** Python 3 · BeautifulSoup · Selenium · boto3 · NewsAPI · AWS Lambda · S3 · CloudWatch  

---

## 1  Project goal

> Crawl six target logistics/supply‑chain web sources + a free news API, push raw + processed JSON to S3, and run the job automatically every day.

## 2  High‑level flow

┌────────────┐ ┌───────────────┐ ┌────────────┐
│ Python Crawlers│→ │ Raw JSON in S3 │→ │ (Option) ETL│
└────────────┘ └───────────────┘ └────────────┘
↘ ↑
↘ AWS Lambda + │
↘ EventBridge (schedule)
↘ │
└─▶ CloudWatch Logs + Alarm (errors≥1)

## 3  Repo layout

.
├─ crawlers/ # one script per site
│ ├─ gnosis.py
│ ├─ logistics_of_logistics.py
│ └─ ...
├─ lambda_newsapi/ # self‑contained NewsAPI Lambda package
│ ├─ lambda_function.py
│ └─ requests/ … # vendored deps
├─ upload_to_s3.py # helper for local dev
├─ requirements.txt
└─ docs/
├─ architecture.png # exported from draw.io / diagrams.net
└─ sample_outputs/

shell
Copy
Edit

## 4  S3 bucket convention

s3://octabyte-data-pipeline/
└── raw/
├── gnosisfreight/
│ └── 2025-07-07/gnosis_2025‑07‑07.json
├── thelogisticsoflogistics/
└── ...

*Each job writes to `raw/<source>/<YYYY‑MM‑DD>/`.*  
Processed/analysed data would live under a future `processed/` prefix.

## 5  Running locally

```bash
python -m venv venv && venv\Scripts\activate   # Windows
pip install -r requirements.txt

# scrape + push one site
python crawlers/gnosis.py
python upload_to_s3.py gnosis_2025‑07‑07.json gnosisfreight

Secrets sit only in .env (never committed).

## 6  Automation on AWS

| Component                    | Why                                                            |
| ---------------------------- | -------------------------------------------------------------- |
| **Lambda `newsapi_crawler`** | grabs news headlines; packaged with `requests` vendored in zip |
| **EventBridge rule**         | triggers the Lambda every day at 03:00 UTC                     |
| **IAM role**                 | minimum ‑ S3 PutObject, CloudWatch Logs                        |
| **CloudWatch alarm**         | notifies on `Errors ≥ 1` via SNS/email                         |

## 7  Extending – add a new site in <3 min

    1. Drop a new script in crawlers/.
    2.Return a list/dict → save to YYYY‑MM‑DD.json.
    3.upload_to_s3.py newfile.json newsource.
    4.(Option) add to an Airflow DAG or another Lambda.

## 8. Future Improvements & Roadmap

The following features were not implemented due to time constraints, but would enhance the pipeline:

- Parallel crawling using Scrapy or asyncio for speed and efficiency.
- Text deduplication and keyword/keyphrase extraction using NLP (e.g., spaCy).
- Dockerized deployment with ECS task scheduling.
- Integration with AWS Athena / QuickSight for queryable reporting and dashboards.
