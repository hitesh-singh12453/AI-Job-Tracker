from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
import os


# Load environment variables from the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Create the SQLAlchemy engine to connect with PostgreSQL
engine = create_engine(DATABASE_URL)


# SessionLocal creates a new database session whenever called
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base is the parent class for all SQLAlchemy ORM models
Base = declarative_base()


# Dependency to provide a database session to API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # Close the database session after the request finishes
        db.close()


"""
Component                  Purpose
------------------------------------------------------------
create_engine()            Connects SQLAlchemy to PostgreSQL
SessionLocal               Creates database sessions
Base                       Parent class for our ORM models
get_db()                   Provides a database session to API endpoints
yield                      Provides the session and allows cleanup
db.close()                 Closes the session after use
"""

""" 
get_db() uses yield because FastAPI handles the dependency lifecycle:
1. A request comes in.
2. A database session is created.
3. The endpoint uses that session.
4. The request finishes.
5. finally executes and closes the session.
"""