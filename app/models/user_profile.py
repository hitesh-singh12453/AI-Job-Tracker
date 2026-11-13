



from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    bio = Column(Text, nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    resume_url = Column(String(255), nullable=True)

    user = relationship(
        "User",
        back_populates="profile"
    )


""" 
cascade="all, delete-orphan" controls what happens to related records when you perform operations on the parent record.
If you delete a parent record, SQLAlchemy also deletes its related child records

"""


""" 
1. unique=True — Correct. It ensures one user can have only one profile. This enforces the one-to-one 
relationship at the database level.

2. uselist=False — Correct. It tells SQLAlchemy to return a single object instead of a list.

3. user.profile — Correct. It returns that user's UserProfile object, containing attributes such as id, user_id, 
bio, linkedin_url, and resume_url.

4. cascade="all, delete-orphan" — Correct. When a user is deleted through SQLAlchemy's ORM, their associated 
profile is deleted too. It also deletes the profile if you remove it from the user's relationship and leave 
it orphaned.
(like parent deleted so it deletes its childs)

"""