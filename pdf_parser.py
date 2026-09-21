import fitz
import re
import json

PDF_FILE = "NEET_PG_2025_Question_Paper_with_Solutions_edf8c1fd790843d752a51ac37b5071a8 (1).pdf"

def extract_questions():
    doc = fitz.open(PDF_FILE)

    text = ""
    for page in doc:
        text += page.get_text()

    pattern = r"(\d+\..*?)(?=\n\d+\.|\Z)"
    matches = re.findall(pattern, text, re.S)

    questions = []

    for q in matches:
        questions.append({
            "raw": q.strip()
        })

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

    print(f"{len(questions)} questions saved.")
