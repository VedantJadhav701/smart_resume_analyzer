import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_country_code(location: str) -> str:
    if "india" in location.lower():
        return "in"
    elif "us" in location.lower() or "united states" in location.lower():
        return "us"
    elif "canada" in location.lower():
        return "ca"
    # Add more mappings if needed
    else:
        return "us"  # default fallback

def load_jobs_from_api(query="machine learning engineer in india", pages=2):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": st.secrets["rapidapi_key"]
    }

    country_code = get_country_code(query)

    all_jobs = []

    for page in range(1, pages + 1):
        params = {
            "query": query,
            "page": str(page),
            "num_pages": "1",
            "country": country_code,
            "date_posted": "all",
            "language": "en"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                st.warning(f"⚠️ Failed to fetch jobs (Status {response.status_code})")
                continue

            jobs = response.json().get("data", [])
            for job in jobs:
                description = job.get("job_description", "")
                # Extract skills from description (implement extract_skills as needed)
                skills = extract_skills(description)
                all_jobs.append({
                    "job_id": job.get("job_id"),
                    "job_title": job.get("job_title"),
                    "company_name": job.get("employer_name"),
                    "location": f"{job.get('job_city', '')}, {job.get('job_country', '')}",
                    "description_text": description,
                    "job_type": ", ".join(job.get("job_employment_types", [])),
                    "date_posted": job.get("job_posted_at_datetime_utc", ""),
                    "apply_link": job.get("job_apply_link", ""),
                    "skills": skills  # Add this line
                })

        except Exception as e:
            st.error(f"❌ API request error: {e}")

    return pd.DataFrame(all_jobs)

def match_jobs(resume_skills, jobs):
    """
    Matches resume skills to jobs.
    Args:
        resume_skills (list): List of skills from the resume.
        jobs (list): List of job dicts with 'skills' key.
    Returns:
        list: Jobs that match the resume skills.
    """
    matched = []
    for job in jobs:
        job_skills = set(job.get('skills', []))
        if job_skills.intersection(resume_skills):
            matched.append(job)
    return matched
