import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf, extract_skills
from job_matcher import load_jobs_from_api, match_jobs
from feedback_generator import generate_feedback

# Define the skill set for extraction
skill_keywords = {'python', 'sql', 'excel', 'ml', 'nlp', 'flask', 'django', 'javascript'}

st.title("📄 Smart Resume Analyzer & Job Recommender")

# Let user enter job query
st.sidebar.header("🔎 Job Search Options")
job_query = st.sidebar.text_input("Job Role", "machine learning engineer")
location = st.sidebar.text_input("Location", "india")
pages = st.sidebar.slider("Number of Pages to Fetch", 1, 5, 2)

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("🧠 Extracted Skills")
    skills = extract_skills(resume_text, skill_keywords)
    st.write(skills if skills else "No known skills found.")

    st.subheader("💼 Recommended Jobs")

    # Load jobs from live API
    query = f"{job_query} in {location}"
    jobs_df = load_jobs_from_api(query=query, pages=pages, skill_keywords=skill_keywords)

    matched_jobs = match_jobs(resume_text, jobs_df)
    st.dataframe(matched_jobs)

    st.subheader("📌 Resume Feedback (LLM Style)")
    with st.spinner("Analyzing with T5 model..."):
        feedback = generate_feedback(resume_text)
        st.write(feedback)
else:
    st.info("📄 Please upload your resume to begin.")
