
""" 
Now we'll create the most important model of our project: JobApplication.

It will store the job applications created by a user.

Before coding, understand the relationship:
- One user can have multiple job applications.
- Each job application belongs to exactly one user.
- Therefore, job_applications.user_id will be a foreign key referencing users.id.

"""

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.associations import application_skills

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    company = Column(String(150), nullable=False)
    role = Column(String(150), nullable=False)
    location = Column(String(150), nullable=True)
    job_type = Column(String(50), nullable=True)
    salary = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False, default="Applied")
    applied_date = Column(Date , nullable=True)
    job_url = Column(String(500) , nullable=True)
    description = Column(Text , nullable=True)
    notes = Column(Text, nullable=True)

    ################### relationships 

    user = relationship("User" , back_populates= "applications")

    """ 
    user.applications in user.py → gets all applications belonging to a user.
    user in user.applications is an instance (object) of the user class 
    applications is relationship attribute defined inside that class

    application.user → gets the user who owns that application. 
    application in application.user is an instance (object) of the JobApplication class.
    """

    interviews = relationship("Interview" , back_populates="application")
    # application.interviews → returns a list of interview records.
    """ 
    application_skills = Table("application_skills" , Base.metadata ,
                            Column("application_id", Integer, ForeignKey("job_applications.id"), primary_key=True),
                            Column("skill_id", Integer, ForeignKey("skills.id") , primary_key=True)
                            ) """ 
    # bcz association is already created in association.py file

    # using association
    skills = relationship("Skill" ,back_populates="applications" , secondary= application_skills)




    application_history = relationship("ApplicationHistory" , back_populates= "application")



