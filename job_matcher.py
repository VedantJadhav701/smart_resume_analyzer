import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# ✅ Match resume text to job descriptions using cosine similarity
def match_jobs(resume_text, jobs_df, top_n=5):
    jobs_df = jobs_df.copy()
    job_descriptions = jobs_df['description_text'].fillna("")

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([resume_text] + job_descriptions.tolist())

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    jobs_df['score'] = similarity_scores

    matched_jobs = jobs_df.sort_values(by='score', ascending=False).head(top_n)
    return matched_jobs[['job_title', 'company_name', 'location', 'apply_link', 'score']]
