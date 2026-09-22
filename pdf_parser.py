import fitz
import re
import json

PDF_FILE = "NEET_PG_2025_Question_Paper_with_Solutions_edf8c1fd790843d752a51ac37b5071a8 (1)(4).pdf"

doc = fitz.open(PDF_FILE)

text = ""
for page in doc:
    text += page.get_text() + "\n"

# Split into questions
blocks = re.split(r"\n(?=\d+\.\s)", text)

questions = []

for block in blocks:

    q = re.search(r"^\d+\.\s(.*?)(?=\n\(A\))", block, re.S)
    opts = re.findall(r"\(([A-D])\)\s(.*)", block)
    ans = re.search(r"Correct Answer:\s*\(([A-D])\)", block)
    sol = re.search(r"Solution:\s*(.*?)(?=\n\d+\.\s|\Z)", block, re.S)

    if not q or len(opts) != 4 or not ans:
        continue

    option_text = [x[1].strip() for x in opts]
    correct = {"A":0,"B":1,"C":2,"D":3}[ans.group(1)]

    questions.append({
        "question": q.group(1).replace("\n"," ").strip(),
        "options": option_text,
        "correct": correct,
        "solution": sol.group(1).strip() if sol else ""
    })

with open("questions.json","w",encoding="utf-8") as f:
    json.dump(questions,f,indent=4,ensure_ascii=False)

print(f"Parsed {len(questions)} questions.")
