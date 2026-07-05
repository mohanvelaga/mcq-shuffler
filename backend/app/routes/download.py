from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

OUTPUT_DIR = Path("app/outputs")

@router.get("/download/{filename}")
def download(filename: str):
    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )