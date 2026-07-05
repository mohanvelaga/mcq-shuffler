from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import os

from app.services.shuffler import shuffle_file

router = APIRouter()

UPLOAD_DIR = Path("app/uploads")
OUTPUT_DIR = Path("app/outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)


class ProcessRequest(BaseModel):
    filename: str


@router.post("/process")
def process(request: ProcessRequest):

    input_path = UPLOAD_DIR / request.filename

    output_path = OUTPUT_DIR / f"jumbled_{request.filename}"

    result = shuffle_file(
        str(input_path),
        str(output_path)
    )

    return {
        "message": "Done",
        "result": result,
        "download": output_path.name
    }