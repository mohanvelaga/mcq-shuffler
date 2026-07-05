from pathlib import Path
import random

import fitz


def shuffle_pdf(input_path: str, output_path: str):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    document = fitz.open(str(input_path))
    blocks = []

    for page in document:
        text = page.get_text().strip()
        if text:
            blocks.extend(line for line in text.splitlines() if line.strip())

    document.close()

    if not blocks:
        raise ValueError("No text content found in PDF file")

    random.shuffle(blocks)

    output_document = fitz.open()
    page = output_document.new_page()
    page.insert_text((72, 72), "\n".join(blocks), fontsize=11)
    output_document.save(str(output_path))
    output_document.close()

    return {
        "processed": len(blocks),
        "output": str(output_path),
    }
