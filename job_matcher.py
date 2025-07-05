import pandas as pd
import requests
import streamlit as st
from collections import Counter
import math

# ✅ Load jobs from RapidAPI (live)
def load_jobs_from_api(query="machine learning engineer in india", pages=2):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": st.secrets["rapidapi_key"]
    }

    all_jobs = []

    for page in range(1, pages + 1):
        params = {
            "query": query,
            "page": str(page),
            "num_pages": "1",
            "country": "us",
            "date_posted": "all",
            "language": "en"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            continue

        for job in response.json().get("data", []):
            all_jobs.append({
                "job_id": job.get("job_id"),
                "job_title": job.get("job_title"),
                "company_name": job.get("employer_name"),
                "location": f"{job.get('job_city', '')}, {job.get('job_country', '')}",
                "description_text": job.get("job_description", ""),
                "job_type": ", ".join(job.get("job_employment_types", [])),
                "date_posted": job.get("job_posted_at_datetime_utc", ""),
                "apply_link": job.get("job_apply_link", "")
            })

    return pd.DataFrame(all_jobs)

# ✅ Pure Python cosine similarity
def cosine_similarity(text1, text2):
    vec1 = Counter(text1.lower().split())
    vec2 = Counter(text2.lower().split())

    intersection = set(vec1) & set(vec2)
    numerator = sum(vec1[x] * vec2[x] for x in intersection)

    sum1 = sum(v ** 2 for v in vec1.values())
    sum2 = sum(v ** 2 for v in vec2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    return float(numerator) / denominator if denominator else 0.0

# ✅ Match jobs using pure Python similarity
def match_jobs(resume_text, jobs_df, top_n=5):
    jobs_df = jobs_df.copy()
    jobs_df["score"] = jobs_df["description_text"].fillna("").apply(lambda desc: cosine_similarity(resume_text, desc))
    matched_jobs = jobs_df.sort_values(by="score", ascending=False).head(top_n)
    return matched_jobs[["job_title", "company_name", "location", "apply_link", "score"]]
