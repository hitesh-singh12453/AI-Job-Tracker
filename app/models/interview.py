


from sqlalchemy import Column, Integer, String, Text, ForeignKey  , DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer , ForeignKey("job_applications.id") , nullable=False)
    round_name = Column(String(50) ,nullable=False)
    interview_date = Column(DateTime(timezone=True), nullable=False)
    feedback = Column(Text )
    outcome = Column(String(50) , default = "Pending" , nullable=False)


    ## relationships 

    application = relationship("JobApplication" , back_populates="interviews")  #Each Interview belongs to exactly one JobApplication.
    