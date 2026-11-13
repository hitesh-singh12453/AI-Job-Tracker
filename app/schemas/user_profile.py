
from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserProfileCreate(BaseModel):
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
