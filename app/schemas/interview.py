
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class InterviewCreate(BaseModel):
    round_name: str
    interview_date: datetime
    feedback: Optional[str] = None
    outcome: Optional[str] = "Pending"


class InterviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    round_name: str
    interview_date: datetime
    feedback: Optional[str] = None
    outcome: str
