from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db


# OAuth2 scheme to extract the Bearer token from incoming requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Recommended password hashing algorithm (Argon2)
password_hash = PasswordHash.recommended()


# ---------------- PASSWORD HASHING ----------------

# Hash the user's password during registration
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# Verify the entered password against the stored hashed password during login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# ---------------- JWT TOKEN CREATION ----------------

def create_access_token(data: dict):
    # Copy the original data so we don't modify the original dictionary
    to_encode = data.copy()

    # Set token expiration time
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiration time to JWT payload
    to_encode.update({"exp": expire})

    # Encode and digitally sign the JWT using SECRET_KEY
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# ---------------- GET CURRENT LOGGED-IN USER ----------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    # Local import to avoid circular import problems
    from app.services.user_service import get_user_by_id

    try:
        # Decode JWT and verify its signature and expiration
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extract user ID from the JWT subject
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Convert user ID into an integer
        user_id = int(user_id)

    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Find the user in the database
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


"""
PASSWORD HASHING DURING REGISTRATION

hashed = hash_password(user_data.password)

new_user = User(
    name=user_data.name,
    email=user_data.email,
    hashed_password=hashed
)

db.add(new_user)
db.commit()
db.refresh(new_user)


PASSWORD VERIFICATION DURING LOGIN

if not verify_password(
    login_data.password,
    user.hashed_password
):
    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )
"""