from fastapi import FastAPI
from app.database import engine
from app.routers import auth, applications
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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