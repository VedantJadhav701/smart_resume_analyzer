import requests
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

def fetch_jobs_to_csv(query="developer jobs in chicago", total_pages=5, filename="data/latest_job_listings.csv"):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": "fd8f167b18mshbfc591ac5310f61p111502jsn852e6387bfbb"
    }

    all_jobs = []

    for page in range(1, total_pages + 1):
        params = {
            "query": query,
            "page": str(page),
            "num_pages": "1",  # Always keep this 1 — you control how many pages you loop
            "country": "us",
            "date_posted": "all",
            "language": "en"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ Error on page {page}: {response.status_code}")
            continue

        data = response.json().get("data", [])
        print(f"✅ Page {page} - {len(data)} jobs")

        for job in data:
            all_jobs.append({
                "job_id": job.get("job_id"),
                "job_title": job.get("job_title"),
                "company_name": job.get("employer_name"),
                "location": f"{job.get('job_city', '')}, {job.get('job_country', '')}",
                "description_text": job.get("job_description", ""),
                "job_type": ", ".join(job.get("job_employment_types", [])),
                "date_posted": job.get("job_posted_at_datetime_utc", ""),
                "apply_link": job.get("job_apply_link", ""),
                "company_website": job.get("employer_website", ""),
                "job_publisher": job.get("job_publisher", "")
            })

    df = pd.DataFrame(all_jobs)
    df.to_csv(filename, index=False)
    print(f"\n📝 Saved {len(df)} total jobs to {filename}")

# Example use
if __name__ == "__main__":
    fetch_jobs_to_csv(query="machine learning engineer in india", total_pages=5)  # Fetches ~50 jobs
