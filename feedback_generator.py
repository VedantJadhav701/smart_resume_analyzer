from transformers import pipeline

# Force TensorFlow backend (not torch)
summarizer = pipeline("summarization", model="t5-small", framework="tf")

def generate_feedback(resume_text):
    if len(resume_text.split()) < 30:
        return "Resume content too short to analyze."

    # Clip input to 1000 characters
    resume_text = resume_text[:1000]

    summary = summarizer(resume_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']
