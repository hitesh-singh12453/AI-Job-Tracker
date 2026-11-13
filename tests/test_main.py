from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

""" 
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Job Tracker API is running"
    }

"""

""" 
Previously, you created TestClient globally. Now client comes from the client fixture in conftest.py
"""
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Job Tracker API is running"
    }



##################################################### registration API test

def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Test12345"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data



# 
def test_register_duplicate_email(client):
    user_data = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "Test12345"
    }

    # First registration should succeed
    response1 = client.post("/auth/register", json=user_data)
    assert response1.status_code == 200

    # Second registration with the same email should fail
    response2 = client.post("/auth/register", json=user_data)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"


############################################## Next: Login API testing.

def test_login_success(client):
    # First, register a user
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "Test12345"
        }
    )

    # Now, login with the same credentials
    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "Test12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

# 2 — Test incorrect password
def test_login_wrong_password(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "wrongpass@example.com",
            "password": "Test12345"
        }
    )

    # Login with incorrect password
    response = client.post(
        "/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

# Test unregistered email
def test_login_unregistered_email(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "unknown@example.com",
            "password": "Test12345"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"



########################################################### Next: Test protected endpoint /auth/me

def test_get_current_user(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Current User",
            "email": "current@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "current@example.com",
            "password": "Test12345"
        }
    )

    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "current@example.com"
    assert "hashed_password" not in response.json()


## Test access without a token

def test_get_current_user_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401

# Test an invalid JWT
def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401



########################################## Job Application API testing,
""" 
again register , login bcz  POST /applications/ endpoint is a protected endpoint.
"""


def test_create_application(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Application User",
            "email": "appuser@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "appuser@example.com",
            "password": "Test12345"
        }
    )

    token = login_response.json()["access_token"]

    # Create application
    response = client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company": "Google",
            "role": "Python Backend Developer",
            "location": "Bangalore",
            "job_type": "Full-time",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-11",
            "job_url": "https://example.com/job",
            "description": "Backend developer position",
            "notes": "Applied through company website"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Google"
    assert data["role"] == "Python Backend Developer"
    assert data["status"] == "Applied"
    assert "id" in data
    assert "user_id" in data



# Test getting all applications
def test_get_all_applications(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Applications User",
            "email": "allapps@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "allapps@example.com",
            "password": "Test12345"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create first application
    client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Google",
            "role": "Python Developer",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    # Create second application
    client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "salary": 1800000,
            "status": "Interview",
            "applied_date": "2026-11-10"
        }
    )

    # Get all applications
    response = client.get("/applications/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["company"] == "Google"
    assert response.json()[1]["company"] == "Microsoft"



# Test getting an application by ID

def test_get_application_by_id(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Single App User",
            "email": "singleapp@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "singleapp@example.com",
            "password": "Test12345"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create application
    create_response = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Amazon",
            "role": "Python Engineer",
            "salary": 1800000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    application_id = create_response.json()["id"]

    # Get application by ID
    response = client.get(
        f"/applications/{application_id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Amazon"


# test updating an application

def test_update_application(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Update User",
            "email": "update@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "update@example.com",
            "password": "Test12345"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create application
    create_response = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Google",
            "role": "Python Developer",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    application_id = create_response.json()["id"]

    # Update application
    response = client.put(
        f"/applications/{application_id}",
        headers=headers,
        json={
            "company": "Google",
            "role": "Senior Python Developer",
            "salary": 2000000,
            "status": "Interview",
            "applied_date": "2026-11-11"
        }
    )

    assert response.status_code == 200
    assert response.json()["role"] == "Senior Python Developer"
    assert response.json()["salary"] == 2000000
    assert response.json()["status"] == "Interview"



## Test successful deletion

def test_delete_application(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Delete User",
            "email": "delete@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "delete@example.com",
            "password": "Test12345"
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create application
    create_response = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Amazon",
            "role": "Backend Developer",
            "salary": 1800000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    application_id = create_response.json()["id"]

    # Delete application
    response = client.delete(
        f"/applications/{application_id}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Application deleted successfully"

    # Verify application is actually deleted
    get_response = client.get(
        f"/applications/{application_id}",
        headers=headers
    )

    assert get_response.status_code == 404




##################################################v   User ownership and security testing

""" 
We'll test:
1. User B cannot view User A's application.
2. User B cannot update User A's application.
3. User B cannot delete User A's application.
"""

# Let's test viewing another user's application first.

def test_user_cannot_access_other_users_application(client):
    # Register User A
    client.post(
        "/auth/register",
        json={
            "name": "User A",
            "email": "usera@example.com",
            "password": "Test12345"
        }
    )

    # Login User A
    login_a = client.post(
        "/auth/login",
        data={
            "username": "usera@example.com",
            "password": "Test12345"
        }
    )

    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User A creates application
    create_response = client.post(
        "/applications/",
        headers=headers_a,
        json={
            "company": "Google",
            "role": "Python Developer",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    application_id = create_response.json()["id"]

    # Register User B
    client.post(
        "/auth/register",
        json={
            "name": "User B",
            "email": "userb@example.com",
            "password": "Test12345"
        }
    )

    # Login User B
    login_b = client.post(
        "/auth/login",
        data={
            "username": "userb@example.com",
            "password": "Test12345"
        }
    )

    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B tries to access User A's application
    response = client.get(
        f"/applications/{application_id}",
        headers=headers_b
    )

    assert response.status_code == 404



# Test unauthorized update

def test_user_cannot_update_other_users_application(client):
    # Register User A
    client.post(
        "/auth/register",
        json={
            "name": "User A",
            "email": "updatea@example.com",
            "password": "Test12345"
        }
    )

    # Login User A
    login_a = client.post(
        "/auth/login",
        data={
            "username": "updatea@example.com",
            "password": "Test12345"
        }
    )

    headers_a = {
        "Authorization": f"Bearer {login_a.json()['access_token']}"
    }

    # User A creates application
    create_response = client.post(
        "/applications/",
        headers=headers_a,
        json={
            "company": "Google",
            "role": "Python Developer",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    application_id = create_response.json()["id"]

    # Register User B
    client.post(
        "/auth/register",
        json={
            "name": "User B",
            "email": "updateb@example.com",
            "password": "Test12345"
        }
    )

    # Login User B
    login_b = client.post(
        "/auth/login",
        data={
            "username": "updateb@example.com",
            "password": "Test12345"
        }
    )

    headers_b = {
        "Authorization": f"Bearer {login_b.json()['access_token']}"
    }

    # User B tries to update User A's application
    response = client.put(
        f"/applications/{application_id}",
        headers=headers_b,
        json={
            "company": "Google",
            "role": "Hacked Developer",
            "salary": 9999999,
            "status": "Selected",
            "applied_date": "2026-11-11"
        }
    )

    assert response.status_code == 404



# Test unauthorized deletion

def test_user_cannot_delete_other_users_application(client):
    # Register User A
    client.post(
        "/auth/register",
        json={
            "name": "User A",
            "email": "deletea@example.com",
            "password": "Test12345"
        }
    )

    # Login User A
    login_a = client.post(
        "/auth/login",
        data={
            "username": "deletea@example.com",
            "password": "Test12345"
        }
    )

    headers_a = {
        "Authorization": f"Bearer {login_a.json()['access_token']}"
    }

    # User A creates application
    create_response = client.post(
        "/applications/",
        headers=headers_a,
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "salary": 1800000,
            "status": "Applied",
            "applied_date": "2026-11-11"
        }
    )

    application_id = create_response.json()["id"]

    # Register User B
    client.post(
        "/auth/register",
        json={
            "name": "User B",
            "email": "deleteb@example.com",
            "password": "Test12345"
        }
    )

    # Login User B
    login_b = client.post(
        "/auth/login",
        data={
            "username": "deleteb@example.com",
            "password": "Test12345"
        }
    )

    headers_b = {
        "Authorization": f"Bearer {login_b.json()['access_token']}"
    }

    # User B tries to delete User A's application
    response = client.delete(
        f"/applications/{application_id}",
        headers=headers_b
    )

    assert response.status_code == 404

    # Verify User A's application still exists
    get_response = client.get(
        f"/applications/{application_id}",
        headers=headers_a
    )

    assert get_response.status_code == 200



######################################################## Next: Test application filters

# Test status filtering
""" 
What are we verifying?
- Two applications exist with different statuses.
- We request only Interview applications.
- The API returns exactly one application.
- That application belongs to Microsoft.
Notice that your filter uses .lower(), so interview, INTERVIEW, and Interview should all work.
"""

def test_filter_applications_by_status(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Filter User",
            "email": "filter@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "filter@example.com",
            "password": "Test12345"
        }
    )

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create first application
    response1 = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Google",
            "role": "Python Developer",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-10"
        }
    )

    # Create second application
    response2 = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "salary": 1800000,
            "status": "Interview",
            "applied_date": "2026-11-11"
        }
    )

    

    # Filter applications by status
    response = client.get(
        "/applications/?status=Interview",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["company"] == "Microsoft"
    assert response.json()[0]["status"] == "Interview"



# search by company or role

def test_search_applications(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Search User",
            "email": "search@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "search@example.com",
            "password": "Test12345"
        }
    )

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create first application
    client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Google",
            "role": "Python Developer",
            "salary": 1500000,
            "status": "Applied",
            "applied_date": "2026-11-10"
        }
    )

    # Create second application
    client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "salary": 1800000,
            "status": "Interview",
            "applied_date": "2026-11-11"
        }
    )

    # Search by company
    response_company = client.get(
        "/applications/?search=goog",
        headers=headers
    )

    assert response_company.status_code == 200
    assert len(response_company.json()) == 1
    assert response_company.json()[0]["company"] == "Google"

    # Search by role
    response_role = client.get(
        "/applications/?search=backend",
        headers=headers
    )

    assert response_role.status_code == 200
    assert len(response_role.json()) == 1
    assert response_role.json()[0]["role"] == "Backend Developer"



#############################################  Next: Pagination test

""" 
We'll verify that skip and limit return the correct subset of applications.
"""

def test_pagination_applications(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Pagination User",
            "email": "pagination@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "pagination@example.com",
            "password": "Test12345"
        }
    )

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create three applications
    companies = ["Google", "Microsoft", "Amazon"]

    for company in companies:
        client.post(
            "/applications/",
            headers=headers,
            json={
                "company": company,
                "role": "Python Developer",
                "salary": 1500000,
                "applied_date": "2026-11-10"
            }
        )

    # Get first two applications
    response = client.get(
        "/applications/?skip=0&limit=2",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2

    # Skip first application and get next two
    response = client.get(
        "/applications/?skip=1&limit=2",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2




#################################################  Next: Sorting test
""" 
We'll verify ascending and descending sorting by company name.
"""
def test_sort_applications_by_company(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Sort User",
            "email": "sort@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "sort@example.com",
            "password": "Test12345"
        }
    )

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create applications
    for company in ["Google", "Amazon", "Microsoft"]:
        client.post(
            "/applications/",
            headers=headers,
            json={
                "company": company,
                "role": "Python Developer",
                "salary": 1500000,
                "applied_date": "2026-11-10"
            }
        )

    # Ascending order
    response = client.get(
        "/applications/?sort_by=company&order=asc",
        headers=headers
    )

    assert response.status_code == 200
    companies = [app["company"] for app in response.json()]
    assert companies == ["Amazon", "Google", "Microsoft"]

    # Descending order
    response = client.get(
        "/applications/?sort_by=company&order=desc",
        headers=headers
    )

    assert response.status_code == 200
    companies = [app["company"] for app in response.json()]
    assert companies == ["Microsoft", "Google", "Amazon"]



########################################## Next: Validate invalid sorting parameters

""" 
We should verify that the API rejects unsupported sort fields 
and invalid sort orders instead of silently accepting them.
"""


def test_invalid_sort_parameters(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Invalid Sort User",
            "email": "invalidsort@example.com",
            "password": "Test12345"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "invalidsort@example.com",
            "password": "Test12345"
        }
    )

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Invalid sort field
    response = client.get(
        "/applications/?sort_by=invalid_field",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid sort field"

    # Invalid sort order
    response = client.get(
        "/applications/?order=random",
        headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid sort order"



#################################################  Next: Final test-suite verification

# Run the complete suite once:
