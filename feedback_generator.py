from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load tokenizer & model (T5-small)
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

def generate_feedback(resume_text):
    if len(resume_text.split()) < 30:
        return "Resume content too short to analyze."

    resume_text = resume_text[:1000]
    input_text = "summarize: " + resume_text

    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    output = model.generate(**inputs, max_length=100, min_length=30, do_sample=False)

    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary
