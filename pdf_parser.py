import fitz
import json

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

if __name__ == "__main__":
    text = extract_text("sample.pdf")
    print(text[:1000])
