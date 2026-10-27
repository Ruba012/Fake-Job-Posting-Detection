from fastapi import APIRouter, HTTPException
from backend.schemas import FeedbackRequest
from backend.database_manager import add_feedback, get_all_feedback
import sqlite3

router = APIRouter()


@router.post("/feedback")
def submit_feedback(data: FeedbackRequest):
    if not data.feedback.strip():
        raise HTTPException(status_code=400, detail="Feedback cannot be empty")

    # Temporary default user until full user handling is added
    user_id = 1

    try:
        contact_value = data.contact.strip() if data.contact and data.contact.strip() else None

        add_feedback(
            user_id=user_id,
            post_id=data.job_id,
            contact=contact_value,
            message=data.feedback
        )

        return {"message": "Feedback submitted successfully"}

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job_id. Make sure the job exists before submitting feedback."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feedback")
def get_feedback():
    try:
        feedback_rows = get_all_feedback()

        formatted_feedback = []
        for row in feedback_rows:
            formatted_feedback.append({
                "feedback_id": row[0],
                "user_id": row[1],
                "post_id": row[2],
                "contact": row[3],
                "message": row[4],
                "created_at": row[5]
            })

        return formatted_feedback

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))