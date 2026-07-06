import random
import fitz  # PyMuPDF

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


# -----------------------------
# CONFIG
# -----------------------------
LEFT_MARGIN = 50
OPTION_MARGIN = 70
TOP_MARGIN = 50
BOTTOM_MARGIN = 60
QUESTION_FONT = "Helvetica-Bold"
OPTION_FONT = "Helvetica"
QUESTION_SIZE = 12
OPTION_SIZE = 11
LINE_HEIGHT = 18
MAX_WIDTH = 470


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_questions(pdf_path):
    """Extract text from PDF."""

    try:
        with fitz.open(pdf_path) as doc:
            text = ""

            for page in doc:
                text += page.get_text("text")
                text += "\n"

        return text.splitlines()

    except Exception as e:
        raise Exception(f"Unable to read PDF: {e}")


# -----------------------------
# PARSER
# -----------------------------
def parse_questions(lines):
    """
    Supports:

    <question> Question text

    <variant> Option 1
    <variant> Option 2
    """

    questions = []

    current_question = None
    current_options = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Question
        if line.startswith("<question>"):

            # Save previous question
            if current_question and current_options:
                questions.append({
                    "question": current_question,
                    "options": current_options
                })

            current_question = line.replace("<question>", "").strip()
            current_options = []

        # Option
        elif line.startswith("<variant>"):

            option = line.replace("<variant>", "").strip()

            if option:
                current_options.append(option)

    # Save last question
    if current_question and current_options:
        questions.append({
            "question": current_question,
            "options": current_options
        })

    return questions


# -----------------------------
# TEXT WRAPPING
# -----------------------------
def wrap_text(text, font, size, width):

    words = text.split()

    if not words:
        return [""]

    lines = []
    current = words[0]

    for word in words[1:]:

        trial = current + " " + word

        if stringWidth(trial, font, size) <= width:
            current = trial
        else:
            lines.append(current)
            current = word

    lines.append(current)

    return lines


# -----------------------------
# WRITE PDF
# -----------------------------
def write_pdf(questions, output_pdf):

    c = canvas.Canvas(output_pdf, pagesize=A4)

    page_width, page_height = A4

    y = page_height - TOP_MARGIN

    for index, q in enumerate(questions, start=1):

        options = q["options"][:]
        random.shuffle(options)

        question_lines = wrap_text(
            f"{index}. {q['question']}",
            QUESTION_FONT,
            QUESTION_SIZE,
            MAX_WIDTH
        )

        option_lines = []

        for option in options:

            wrapped = wrap_text(
                "• " + option,
                OPTION_FONT,
                OPTION_SIZE,
                MAX_WIDTH - 20
            )

            option_lines.extend(wrapped)

        required_height = (
            len(question_lines) * LINE_HEIGHT
            + len(option_lines) * LINE_HEIGHT
            + 30
        )

        # New page if needed
        if y - required_height < BOTTOM_MARGIN:

            c.showPage()

            y = page_height - TOP_MARGIN

        # Question
        c.setFont(QUESTION_FONT, QUESTION_SIZE)

        for line in question_lines:

            c.drawString(LEFT_MARGIN, y, line)

            y -= LINE_HEIGHT

        # Options
        c.setFont(OPTION_FONT, OPTION_SIZE)

        for option in options:

            wrapped = wrap_text(
                "• " + option,
                OPTION_FONT,
                OPTION_SIZE,
                MAX_WIDTH - 20
            )

            for line in wrapped:

                c.drawString(OPTION_MARGIN, y, line)

                y -= LINE_HEIGHT

        y -= 12

    c.save()


# -----------------------------
# MAIN SHUFFLER
# -----------------------------
def shuffle_pdf(input_pdf, output_pdf):

    lines = extract_questions(input_pdf)

    questions = parse_questions(lines)

    if not questions:
        raise ValueError(
            "No MCQs found. Ensure the PDF contains "
            "<question> and <variant> tags."
        )

    write_pdf(questions, output_pdf)

    return {
        "status": "success",
        "questions": len(questions),
        "output": output_pdf
    }