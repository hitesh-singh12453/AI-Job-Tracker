from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base



class ApplicationHistory(Base):
    __tablename__ = "application_history"

    id = Column(Integer , primary_key=True , index=True)
    application_id = Column(Integer , ForeignKey("job_applications.id"),nullable=False )
    old_status = Column(String(50) )
    new_status = Column(String(50))
    changed_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    """ 
    server_default=func.now() means the database automatically inserts the current date and time 
    if you don't provide a value. 
    """

    application = relationship("JobApplication" , back_populates="application_history")
    
