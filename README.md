# AI Job Tracker API

A backend application built with **Python and FastAPI** to help users manage and track their job applications.

The API allows users to register, authenticate, create and manage job applications, track application status, and organize their job search in one place.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing and verification
- Create, read, update, and delete job applications
- Filter and search job applications
- PostgreSQL database integration
- Input validation using Pydantic
- Automated API testing using Pytest

## Technology Stack

- **Language:** Python
- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** JWT
- **Testing:** Pytest
- **Version Control:** Git and GitHub

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and generate JWT token |
| GET | `/auth/me` | Get current authenticated user |

### Job Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/applications/` | Create a new job application |
| GET | `/applications/` | Get all applications belonging to the current user |
| GET | `/applications/{application_id}` | Get a specific application |
| PUT | `/applications/{application_id}` | Update an application |
| DELETE | `/applications/{application_id}` | Delete an application |

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/test-db` | Test database connectivity |

## Installation & Setup

### 1. Clone the repository

```bash
git clone git@github.com:hitesh-singh12453/AI-Job-Tracker.git
cd AI-Job-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the placeholder values with your actual PostgreSQL connection URL and a secure secret key.

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

`http://127.0.0.1:8000`

## Interactive API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Once the application is running, visit:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests

This project uses **Pytest** for automated API testing.

Run all tests:

```bash
pytest
```

For detailed test output:

```bash
pytest -v
```

Pytest will discover and execute the test cases inside the `tests/` directory.

## Project Status

**In Development**

The core backend functionality is implemented, including authentication, job application management, database integration, and automated testing.

Future improvements may include additional job search features, analytics, and AI-powered functionality.