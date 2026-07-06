from pathlib import Path

from app.services.docx_processor import shuffle_docx
from app.services.pdf_processor import shuffle_pdf


def shuffle_file(input_path, output_path):

    ext = Path(input_path).suffix.lower()

    if ext == ".docx":
        return shuffle_docx(input_path, output_path)

    elif ext == ".pdf":
        return shuffle_pdf(input_path, output_path)

    else:
        raise Exception("Unsupported file type")