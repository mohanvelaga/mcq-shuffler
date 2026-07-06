from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.process import router as process_router
from app.routes.upload import router as upload_router, start_cleanup_loop, stop_cleanup_loop
from app.routes.download import router as download_router


app = FastAPI(title="MCQ Shuffler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173","https://mcq-shuffler.vercel.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(download_router)


@app.on_event("startup")
def start_background_cleanup() -> None:
    start_cleanup_loop()


@app.on_event("shutdown")
def stop_background_cleanup() -> None:
    stop_cleanup_loop()