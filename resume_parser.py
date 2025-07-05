import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_skills(text, skill_keywords):
    doc = nlp(text)
    found_skills = set()
    for token in doc:
        if token.text.lower() in skill_keywords:
            found_skills.add(token.text.lower())
    return list(found_skills)
