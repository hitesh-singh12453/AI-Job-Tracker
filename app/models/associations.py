""" 
This file will contain the association table connecting job_applications and skills.

 """
from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database import Base


application_skills = Table(
    "application_skills",
    Base.metadata,

    Column(
        "application_id",
        Integer,
        ForeignKey("job_applications.id"),
        primary_key=True
    ),

    Column(
        "skill_id",
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )
)



""" 
Why Table() instead of a class?

Our association table only connects two tables. It doesn't currently need its own additional attributes, 
so SQLAlchemy's Table() is sufficient.
"""

""" 

3. Can this association table contain the same pair (1, 2) twice?

combination of application_id and skill_id must be unique. Either value can appear multiple times individually  

"""

"""
Composite Primary Key:

(application_id, skill_id) together uniquely identify each row.

This prevents the same skill from being linked to the same
job application more than once.

However:
- One application can have multiple skills.
- One skill can belong to multiple applications.
"""