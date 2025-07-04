import subprocess
import datetime
import os

def run_scraper_and_upload(scraper_script: str, source_name: str):
    # Run scraper
    print(f"Running scraper for {source_name}...")
    result = subprocess.run(["python", scraper_script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running {scraper_script}: {result.stderr}")
        return

    # Prepare file name with today's date
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    file_name = f"{source_name}_{today}.txt"

    # Upload to S3
    print(f"Uploading {file_name} to S3...")
    upload_command = f"python upload_to_s3.py {file_name} {source_name}"
    os.system(upload_command)

if __name__ == "__main__":
    # Add your scrapers here
    scrapers = [
        ("scrape_freightwaves.py", "freightwaves"),
        ("scrape_gnosisfreight.py", "gnosisfreight"),
        # Add more scrapers here as you create them
    ]

    for scraper_script, source_name in scrapers:
        run_scraper_and_upload(scraper_script, source_name)

    print("Pipeline complete!")
