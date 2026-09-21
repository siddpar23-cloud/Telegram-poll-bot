import fitz
import re
import json

questions = []

doc = fitz.open("sample.pdf")

text = ""
for page in doc:
    text += page.get_text()

pattern = r"(\d+\..*?)(?=\n\d+\.|\Z)"

matches = re.findall(pattern, text, re.S)

for item in matches:
    questions.append({
        "raw": item.strip()
    })

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=4, ensure_ascii=False)

print(f"{len(questions)} questions extracted.")
