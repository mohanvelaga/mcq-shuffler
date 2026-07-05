from fastapi import APIRouter, UploadFile, File
import shutil
import os
import threading
import time
import uuid

router = APIRouter()

UPLOAD_DIR = "app/uploads"
OUTPUT_DIR = "app/outputs"
CLEANUP_INTERVAL_SECONDS = 24 * 60 * 60
MAX_FILE_AGE_SECONDS = 24 * 60 * 60

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

_cleanup_stop_event = threading.Event()
_cleanup_thread = None


def cleanup_old_uploads(directory: str = UPLOAD_DIR, max_age_seconds: int = MAX_FILE_AGE_SECONDS) -> int:
    if not os.path.isdir(directory):
        return 0

    removed_count = 0
    now = time.time()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > max_age_seconds:
            os.remove(file_path)
            removed_count += 1

    return removed_count


def start_cleanup_loop() -> None:
    global _cleanup_thread

    for directory in (UPLOAD_DIR, OUTPUT_DIR):
        cleanup_old_uploads(directory)

    if _cleanup_thread and _cleanup_thread.is_alive():
        return

    def run_cleanup_loop() -> None:
        while not _cleanup_stop_event.wait(CLEANUP_INTERVAL_SECONDS):
            for directory in (UPLOAD_DIR, OUTPUT_DIR):
                cleanup_old_uploads(directory)

    _cleanup_stop_event.clear()
    _cleanup_thread = threading.Thread(target=run_cleanup_loop, daemon=True)
    _cleanup_thread.start()


def stop_cleanup_loop() -> None:
    global _cleanup_thread

    if _cleanup_thread and _cleanup_thread.is_alive():
        _cleanup_stop_event.set()
        _cleanup_thread.join(timeout=2)
        _cleanup_thread = None


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    extension = file.filename.split(".")[-1]

    unique_name = f"{uuid.uuid4()}.{extension}"

    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": unique_name,
        "original": file.filename,
        "message": "Upload Successful"
    }