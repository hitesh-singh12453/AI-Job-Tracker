from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import get_user_by_email, create_user

# For password verification and JWT token creation
from app.core.security import (verify_password, create_access_token)

# To protect endpoints and identify the logged-in user
from app.core.security import get_current_user

## to protect endpoint
from app.core.security import get_current_user


from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


""" 
router is obj of APIRouter()
response_model=UserResponse -> tells FastAPI which Pydantic schema to use for the API response
"""


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = create_user(db, user_data)

    return new_user





@router.post("/login")
def login( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, form_data.username)

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



""" 
## earlier befor   OAuth2PasswordRequestForm


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user_data.email)

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


"""



""" 
sub  stand for subject 
- It is a standard JWT claim used to identify who the token belongs to.
- we're storing the user's ID as the subject.
"""



@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user