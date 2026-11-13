from pydantic import BaseModel , ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    created_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str




"""
WHY OAuth2PasswordRequestForm INSTEAD OF UserLogin?

OAuth2PasswordRequestForm follows the OAuth2 password form format
expected by FastAPI's OAuth2 authentication flow.

It receives:
- username: We use this field to receive the user's email.
- password: The user's plain-text password.

LOGIN FLOW:
1. Receive email and password using OAuth2PasswordRequestForm.
2. Find the user in the database using the email.
3. Verify the entered password against the stored Argon2 hash.
4. Generate a JWT access token using create_access_token().
5. Return the access token to the client.

IMPORTANT:
OAuth2PasswordRequestForm only receives credentials.
It does NOT generate the JWT.

create_access_token() generates the JWT.
OAuth2PasswordBearer extracts the Bearer token from future requests.
"""