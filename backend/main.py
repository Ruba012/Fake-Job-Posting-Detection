import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.routes.analyze import router as analyze_router
from backend.routes.feedback import router as feedback_router
from backend.routes.admin import router as admin_router
from backend.database_manager import init_database, ensure_default_user
from backend.utils import load_models

print("USING backend/main.py")

BASE_DIR = os.path.dirname(__file__)
FRONTEND_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "frontend.html"))

app = FastAPI(title="Fake Job Post Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(feedback_router)
app.include_router(admin_router)


@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_PATH)


init_database()
ensure_default_user()
load_models()
