import random
import re
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def extract_questions(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"

    return text.splitlines()


def parse_questions(lines):

    questions = []

    current_question = []
    current_options = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # New Question
        if re.match(r'^\d+[\.\)]', line):

            if current_question:

                questions.append({
                    "question": current_question,
                    "options": current_options
                })

            current_question = [line]
            current_options = []

        # Option
        elif re.match(r'^[A-Da-d][\.\)]', line):

            current_options.append(line)

        else:

            if current_options:
                current_options.append(line)
            else:
                current_question.append(line)

    if current_question:
        questions.append({
            "question": current_question,
            "options": current_options
        })

    return questions


def write_pdf(questions, output_pdf):

    c = canvas.Canvas(output_pdf, pagesize=A4)

    width, height = A4

    y = height - 50

    for q in questions:

        for line in q["question"]:

            c.drawString(50, y, line)

            y -= 18

        options = q["options"]

        random.shuffle(options)

        for option in options:

            c.drawString(70, y, option)

            y -= 18

        y -= 20

        if y < 80:

            c.showPage()

            y = height - 50

    c.save()


def shuffle_pdf(input_pdf, output_pdf):

    lines = extract_questions(input_pdf)

    questions = parse_questions(lines)

    write_pdf(questions, output_pdf)

    return {
        "status": "success",
        "questions": len(questions),
        "output": output_pdf
    }