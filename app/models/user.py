
#  This model stores user account information.

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One-to-Many
    applications = relationship(
        "JobApplication",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # One-to-One
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )



""" 
Code	                                Purpose
unique=True	                        Prevents duplicate email addresses
nullable=False	                    Value cannot be NULL
index=True	                        Creates an index to speed up lookups
func.now()	                        Database-generated creation timestamp
applications	                    Access all applications belonging to a user from JobApplication table
profile	                            Access the user's single profile
cascade	                            Propagates deletion to related records

"""