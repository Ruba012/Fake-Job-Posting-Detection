import os

from fastapi import APIRouter, HTTPException

from backend.database_manager import (
    delete_job,
    get_all_jobs_with_results,
    get_feedback_count,
)
from backend.schemas import LoginRequest

router = APIRouter()


@router.post("/login")
def admin_login(data: LoginRequest):
    expected_username = os.getenv("FJPD_ADMIN_USERNAME")
    expected_password = os.getenv("FJPD_ADMIN_PASSWORD")
    if not expected_username or not expected_password:
        raise HTTPException(status_code=503, detail="Admin login is not configured")

    if data.username == expected_username and data.password == expected_password:
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/records")
def get_records():
    records = get_all_jobs_with_results()

    formatted_records = []
    for row in records:
        formatted_records.append({
            "post_id": row[0],
            "title": row[1],
            "prediction": row[2],
            "confidence": row[3]
        })

    return formatted_records


@router.get("/stats")
def get_stats():
    records = get_all_jobs_with_results()

    total = len(records)
    fake = 0
    real = 0

    for row in records:
        prediction = str(row[2]).strip().lower() if row[2] is not None else ""

        if prediction == "fake":
            fake += 1
        elif prediction == "real":
            real += 1

    fake_rate = round((fake / total) * 100, 1) if total > 0 else 0.0
    feedback_count = get_feedback_count()

    return {
        "total": total,
        "fake_count": fake,
        "real_count": real,
        "fake_rate": fake_rate,
        "feedback_count": feedback_count
    }


@router.delete("/record/{record_id}")
def delete_record(record_id: int):
    delete_job(record_id)
    return {"message": f"Record {record_id} deleted successfully"}
