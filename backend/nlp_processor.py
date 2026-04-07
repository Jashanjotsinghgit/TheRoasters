import spacy
from resume_parser import extract_text
from resume_parser import pdf_path as path
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    doc = nlp(text)
    tokens = [
        token.text.lower()
        for token in doc
        if not token.is_stop and token.is_alpha
    ]
    cleaned_text = " ".join(tokens)
    return cleaned_text


if __name__ == "__main__":

    resume_text = extract_text(path)
    result = process_text(resume_text)
    print(result)