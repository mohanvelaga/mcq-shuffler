from pathlib import Path

from app.services.docx_processor import shuffle_docx
from app.services.pdf_processor import shuffle_pdf


def shuffle_file(input_path: str, output_path: str):
    extension = Path(input_path).suffix.lower()

    if extension == ".docx":
        return shuffle_docx(input_path, output_path)

    if extension == ".pdf":
        return shuffle_pdf(input_path, output_path)

    raise ValueError(f"Unsupported file type: {extension}")