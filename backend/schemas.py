from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    title: str
    text: str


class AnalyzeResponse(BaseModel):
    prediction: str
    confidence: float


class FeedbackRequest(BaseModel):
    job_id: int
    feedback: str
    contact: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str