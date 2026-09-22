import fitz
import re
import json

PDF_FILE = "NEET_PG_2025_Question_Paper_with_Solutions_edf8c1fd790843d752a51ac37b5071a8 (1)(4).pdf"

doc = fitz.open(PDF_FILE)

text = ""
for page in doc:
    text += page.get_text("text") + "\n"

# Split using question numbers
blocks = re.split(r"(?=\n\d+\.\s)", "\n" + text)

questions = []

for block in blocks:

    block = block.strip()

    if not block:
        continue

    # Question
    q_match = re.search(
        r"^\d+\.\s(.*?)(?=\n\(A\))",
        block,
        re.S,
    )

    if not q_match:
        continue

    question = re.sub(r"\s+", " ", q_match.group(1)).strip()

    # Options
    option_matches = re.findall(
        r"\(([A-D])\)\s*(.+?)(?=\n\([A-D]\)|\nCorrect Answer:|\Z)",
        block,
        re.S,
    )

    if len(option_matches) != 4:
        continue

    options = []

    for _, opt in option_matches:
        opt = re.sub(r"\s+", " ", opt).strip()
        options.append(opt)

    # Correct answer
    ans_match = re.search(
        r"Correct Answer:\s*\(([A-D])\)",
        block,
    )

    if not ans_match:
        continue

    correct = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3
    }[ans_match.group(1)]

    # Solution
    sol_match = re.search(
        r"Solution:\s*(.*?)(?=\n\d+\.\s|\Z)",
        block,
        re.S,
    )

    solution = ""

    if sol_match:
        solution = re.sub(
            r"\s+",
            " ",
            sol_match.group(1)
        ).strip()

    questions.append(
        {
            "question": question,
            "options": options,
            "correct": correct,
            "solution": solution,
        }
    )

with open(
    "questions.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        questions,
        f,
        indent=4,
        ensure_ascii=False,
    )

print("=" * 40)
print("Questions Parsed :", len(questions))

if questions:
    print("First :", questions[0]["question"])
    print("Last  :", questions[-1]["question"])

print("=" * 40)
