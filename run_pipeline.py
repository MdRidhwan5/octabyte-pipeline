import subprocess

print("🚀 Running scraper...")
subprocess.run(["python", "scrape_freightwaves.py"])

print("☁️ Uploading to S3...")
subprocess.run(["python", "upload_to_s3.py"])

print("✅ Pipeline complete!")
