from app.models.job_application import JobApplication


# ---------------- CREATE APPLICATION ----------------

def create_application(db, application_data, user_id):

    # Create a new JobApplication object
    new_application = JobApplication(
        company=application_data.company,
        role=application_data.role,
        location=application_data.location,
        job_type=application_data.job_type,
        salary=application_data.salary,
        status=application_data.status,
        description=application_data.description,
        notes=application_data.notes,
        job_url=application_data.job_url,
        applied_date=application_data.applied_date,
        user_id=user_id
    )

    # Save the application in the database
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# ---------------- FETCH ONE APPLICATION ----------------

def get_application_by_id(db, application_id, user_id):

    # Find an application belonging to the logged-in user
    application = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == user_id
        )
        .first()
    )

    return application


# ---------------- FETCH ALL APPLICATIONS ----------------

def get_all_applications(db, user_id):

    # Fetch only applications belonging to the logged-in user
    applications = (
        db.query(JobApplication)
        .filter(JobApplication.user_id == user_id)
        .all()
    )

    return applications


# ---------------- UPDATE APPLICATION ----------------

def update_application(db, application_id, user_id, application_data):

    # Find the application and verify ownership
    application = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == user_id
        )
        .first()
    )

    # Return None if application doesn't exist or belongs to another user
    if application is None:
        return None

    # Update application fields
    application.company = application_data.company
    application.role = application_data.role
    application.location = application_data.location
    application.job_type = application_data.job_type
    application.salary = application_data.salary
    application.status = application_data.status
    application.description = application_data.description
    application.notes = application_data.notes
    application.job_url = application_data.job_url
    application.applied_date = application_data.applied_date

    # Save updated values
    db.commit()
    db.refresh(application)

    return application


# ---------------- DELETE APPLICATION ----------------

def delete_application(db, application_id, user_id):

    # Find the application and verify ownership
    application = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == user_id
        )
        .first()
    )

    # Return False if application doesn't exist or belongs to another user
    if application is None:
        return False

    db.delete(application)
    db.commit()

    return True