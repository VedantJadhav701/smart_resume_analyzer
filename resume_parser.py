import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text, skill_keywords):
    doc = nlp(text)
    found_skills = set()
    for token in doc:
        if token.text.lower() in skill_keywords:
            found_skills.add(token.text.lower())
    return list(found_skills)
