
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationResponse
)
from app.services import job_application_service


router = APIRouter(
    prefix="/applications",
    tags=["Job Applications"]
)


# ---------------- CREATE APPLICATION ----------------

@router.post(
    "/",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_application(
    application_data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_application = job_application_service.create_application(
        db,
        application_data,
        current_user.id
    )

    return new_application


"""
@router.post("/") — creates a new application.
application_data — receives and validates the request body.
Depends(get_db) — provides the database session.
Depends(get_current_user) — verifies JWT and gets the logged-in user.
current_user.id — associates this application with that user.
response_model — validates and formats the response.
201 CREATED
"""


# ---------------- FETCH ALL APPLICATIONS ----------------

@router.get("/", response_model=list[JobApplicationResponse])
def get_my_applications(
    status: str = None,
    search: str = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    sort_by: str = "applied_date",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Fetch only the logged-in user's applications
    applications = job_application_service.get_all_applications(
        db,
        current_user.id
    )

    # Filter applications by status
    if status:
        applications = [
            application
            for application in applications
            if application.status.lower() == status.lower()
        ]

    # Search by company name or job role
    if search:
        applications = [
            application
            for application in applications
            if search.lower() in application.company.lower()
            or search.lower() in application.role.lower()
        ]

    # Validate sorting field
    if sort_by not in ["company", "salary", "applied_date"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    # Validate sorting order
    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort order"
        )

    # Sort applications
    applications.sort(
        key=lambda application: (
            getattr(application, sort_by) is None,
            getattr(application, sort_by)
        ),
        reverse=(order.lower() == "desc")
    )

    # Apply pagination after filtering and sorting
    return applications[skip : skip + limit]


"""
Important concepts:

status: str = None
Makes status an optional query parameter.

if status:
Only applies the status filter when the user provides a status.

application = [...]
This is a list comprehension.

Partial matching:
search.lower() in application.company.lower()

This allows searches such as "goog" to match "Google".

getattr(object, attribute_name)
Gets an object's attribute dynamically.

For example:
getattr(application, "company")
is equivalent to:
application.company

Pagination:
applications[skip : skip + limit]

Filtering → Sorting → Pagination
"""


# ---------------- FETCH ONE APPLICATION ----------------

@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    application = job_application_service.get_application_by_id(
        db,
        application_id,
        current_user.id
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application


"""
JobApplication.id == application_id
JobApplication.user_id == user_id

Checking both prevents User A from accessing User B's
applications just by guessing their application ID.
"""


# ---------------- UPDATE APPLICATION ----------------

@router.put(
    "/{application_id}",
    response_model=JobApplicationResponse
)
def update_application(
    application_id: int,
    application_data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_application = job_application_service.update_application(
        db,
        application_id,
        current_user.id,
        application_data
    )

    if not updated_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return updated_application


"""
Understand the flow:

1. Receive the application ID.
2. Receive updated application data.
3. Verify the JWT.
4. Pass the authenticated user's ID to the service.
5. Service finds the application belonging to that user.
6. Update and return the record.
"""


# ---------------- DELETE APPLICATION ----------------

@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = job_application_service.delete_application(
        db,
        application_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "message": "Application deleted successfully"
    }
