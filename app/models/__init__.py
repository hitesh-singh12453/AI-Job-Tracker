
## importing models 

from app.models.associations import application_skills
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.job_application import JobApplication
from app.models.interview import Interview
from app.models.skill import Skill
from app.models.application_history import ApplicationHistory


"""
WHY DO WE IMPORT ALL MODELS HERE?

SQLAlchemy needs to know about all model classes before
creating database tables using:

    Base.metadata.create_all(bind=engine)

Importing these models registers their tables with Base.metadata.

Without importing a model, SQLAlchemy may not know that the
model's table exists when create_all() is executed.

MODEL REGISTRATION:
1. User
2. UserProfile
3. JobApplication
4. Interview
5. Skill
6. ApplicationHistory
7. application_skills (association table)

IMPORTANT:
Import models before calling create_all().

We keep create_all() disabled in main.py because our application
uses a separate test database and we don't want to create tables
automatically in the development database during app imports.
"""
