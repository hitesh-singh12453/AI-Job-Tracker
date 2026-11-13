
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


# ---------------- INCOMING REQUEST DATA ----------------

class JobApplicationCreate(BaseModel):
    company: str
    role: str

    # Optional means the field can contain its specified data type or None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    job_url: Optional[str] = None

    # SQLAlchemy uses Date, so we use Python's date type here
    applied_date: Optional[date] = None


# ---------------- OUTGOING RESPONSE DATA ----------------

class JobApplicationResponse(BaseModel):

    # Allows Pydantic to read data directly from SQLAlchemy model attributes
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    company: str
    role: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[int] = None

    # Application status is expected to be a string
    status: str

    description: Optional[str] = None
    notes: Optional[str] = None
    job_url: Optional[str] = None
    applied_date: Optional[date] = None


"""
IMPORTANT CONCEPTS

1. JobApplicationCreate:
   - Defines the data accepted from the client.
   - company and role are required.
   - Other fields are optional.
   - user_id is not accepted from the client.
   - The backend gets user_id from the authenticated user.

2. JobApplicationResponse:
   - Defines the data returned to the client.
   - Includes database-generated id and user_id.
   - Does not expose sensitive information.

3. ConfigDict(from_attributes=True):
   - Allows Pydantic to read values from SQLAlchemy ORM objects.
   - We don't need to manually convert every database object into a dictionary.

4. applied_date:
   - Uses Python date because the SQLAlchemy model uses Column(Date).

5. status:
   - The incoming status can be omitted.
   - The SQLAlchemy model has the default status "Applied".
"""
