# 🧪 Testing Report – Web Crawling Pipeline

**Tested By:** Md Ridhwan  
**Date:** 2025-07-08  
**Environment:** Local (Windows 10), Python 3.11, AWS Free Tier

---

## ✅ 1. Test: Sample Crawled Data per Source

Each crawler script was executed and collected **≥10 data entries**. Sample outputs are stored under `docs/sample_outputs/`.

| Source                      | File Name                                           | Articles Count |
|-----------------------------|-----------------------------------------------------|----------------|
| Gnosis Freight              | gnosisfreight_2025-07-04.json                       | 12             |
| The Logistics of Logistics  | thelogisticsoflogistics_2025-07-04.json             | 11             |
| FreightWaves                | freightwaves_2025-07-04.json                        | 13             |
| LeadIQ                      | leadiq_2025-07-07.json                              | 10             |
| G2 Reviews (Gnosis)         | sell_g2_com_content_20250707_164451.json            | 15             |
| Markets and Markets         | marketsandmarkets_supplychain_20250707_170606.json  | 10             |
| NewsAPI                     | newsapi_logistics_20250707_195509.json              | 20             |

✅ *All crawlers successfully fetched more than 10 records.*

---

## 🔄 2. Test: Incremental Updates (Deduplication)

**Logic Used:**  
- Each crawler saves output as `source_YYYY-MM-DD.json`.  
- S3 key is based on that structure: `raw/<source>/<YYYY-MM-DD>/`.

**Method to check:**  
- Ran the same script twice in one day → no overwrite on S3 (versioned).
- Used SHA256 checksum (or timestamp) to identify new vs. duplicate entries.

**Example:**
- `thelogisticsoflogistics_2025-07-04.json` (created at 10:00 AM)
- `thelogisticsoflogistics_2025-07-04.json` (created again at 6:00 PM)

Only new/unique entries were uploaded. Identical entries were skipped.

---

## 🧪 3. Manual QA Verification

- Verified all JSON files are valid via [https://jsonlint.com](https://jsonlint.com)
- NewsAPI integration correctly filtered for keywords like `logistics`, `freight`, `supply chain`
- Selenium pages (like G2, MarketsAndMarkets) handled dynamic content successfully
- Files uploaded to correct S3 structure: `s3://octabyte-data-pipeline/raw/source/date/`

---

## 📌 Notes

- In future, deduplication can be enhanced using UUID or content hashes.
- Logs from AWS Lambda are visible in **CloudWatch Logs**.
- Alarms are triggered if function errors exceed 1 per run.

---
