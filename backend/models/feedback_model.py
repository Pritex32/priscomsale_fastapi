from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class FeedbackRequest(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    feedback: str

class FeedbackResponse(FeedbackRequest):
    feedback_id: int
    created_at: datetime
