from transformers import pipeline

# Load the summarization pipeline with T5 model
summarizer = pipeline("summarization", model="t5-small")

def generate_feedback(resume_text):
    # Ensure text is not too short
    if len(resume_text.split()) < 30:
        return "Resume content too short to analyze."

    # T5 has a 512-token limit for input — we’ll clip text
    resume_text = resume_text[:1000]

    # Generate summary/feedback
    summary = summarizer(resume_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']
