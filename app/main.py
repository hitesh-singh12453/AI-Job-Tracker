from fastapi import FastAPI
from app.database import engine
from app.routers import auth, applications


app = FastAPI()

# Register application routers after creating the FastAPI app
app.include_router(applications.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "AI Job Tracker API is running"}


# Check whether the API can connect to PostgreSQL
@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            return {"message": "PostgreSQL connected successfully"}
    except Exception as e:
        return {"error": str(e)}


# Create database tables automatically (currently disabled)
# Base.metadata.create_all(bind=engine)