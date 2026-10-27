from fastapi import APIRouter, HTTPException
from backend.schemas import AnalyzeRequest, AnalyzeResponse
from backend.utils import predict_job
from backend.database_manager import add_job_post, add_analysis_result

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job(data: AnalyzeRequest):
    # Reject empty input
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Run prediction using backend model pipeline
        prediction, confidence = predict_job(data.title, data.text)

        # Make sure confidence is a float and rounded cleanly
        confidence = round(float(confidence), 4)

        # Temporary default user until full user system is added
        user_id = 1

        # Store submitted job post in database
        post_id = add_job_post(data.title, data.text, user_id)

        # Store prediction result in database
        add_analysis_result(post_id, prediction, confidence)

        # Return API response
        return AnalyzeResponse(
            prediction=prediction,
            confidence=confidence
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))