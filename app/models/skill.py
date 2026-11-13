

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100) ,nullable=False , unique=True )

    applications = relationship("JobApplication" , back_populates="skills" , secondary="application_skills")
