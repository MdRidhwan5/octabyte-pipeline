# 🧠 Architecture Overview – Octa Byte AI Pipeline

This document outlines the architecture and key components of the web crawling pipeline built for logistics & supply chain data ingestion.

---

## 🔧 Components

| Layer             | Tools/Tech Used                                | Purpose                                                             |
|------------------|--------------------------------------------------|---------------------------------------------------------------------|
| Crawling         | Python (Selenium / BeautifulSoup)               | Extract web page content from 6 logistics sites                     |
| News Integration | NewsAPI (via `requests`)                        | Fetch latest news articles on logistics/supply chain                |
| Storage          | AWS S3                                          | Store raw HTML/JSON and processed clean text                        |
| Orchestration    | AWS Lambda + EventBridge                        | Run news crawler daily at 3:00 AM UTC                               |
| Monitoring       | AWS CloudWatch (logs + alarms)                  | Monitor Lambda health and alert on errors                          |
| Access Control   | IAM Roles                                       | Secure access to S3 and CloudWatch                                  |

---

## 📐 Data Flow

```mermaid
graph TD
    A[Crawlers: BeautifulSoup/Selenium] --> B[Raw JSON]
    B --> C[S3: octabyte-data-pipeline/raw/source/date]
    A --> D[AWS Lambda (newsapi)]
    D --> E[CloudWatch Logs]
    E --> F[CloudWatch Alarm (Errors >= 1)]
    G[EventBridge Scheduler] --> D
        D --> H[CloudWatch Logs]
        H --> I[Alarm if Errors >= 1]
    end

    C -->|PutObject| S3[(S3 Bucket)]
    F -->|PutObject| S3
````

---

## 📁 S3 Bucket Structure

```
s3://octabyte-data-pipeline/
└── raw/
    ├── gnosisfreight/
    │   └── 2025-07-07/gnosis_2025-07-07.json
    ├── freightwaves/
    ├── newsapi/
    │   └── 2025-07-07/newsapi_2025-07-07.json
    └── ...
```

* Data is written daily using this convention:
  `raw/<source>/<YYYY-MM-DD>/<source>_<date>.json`

---

## 🧩 Extensibility

* Each crawler is modular — you can add a new source by:

  1. Dropping a new `.py` in `crawlers/`
  2. Making it return a JSON file
  3. Running the uploader with `upload_to_s3.py`
  4. (Optional) Automating via Lambda/Airflow

---

## ⚠️ Monitoring

* **Logs:** CloudWatch automatically captures all Lambda logs.
* **Alarms:** Configured to notify if function errors ≥ 1.

---

## 🔒 Security

* `.env` never committed (listed in `.gitignore`)
* IAM user has only scoped permissions for `PutObject`, logs

---

© 2025 Octa Byte AI Pvt Ltd – Confidential