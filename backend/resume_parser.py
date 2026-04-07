import pdfplumber
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(script_dir)
pdf_path = os.path.join(BASE_DIR, "model_input_resumes", "jashan_resume.pdf")
print(pdf_path)

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return (text)

extract_text(pdf_path)