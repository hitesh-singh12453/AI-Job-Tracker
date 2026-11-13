from app.models.user import User
from app.core.security import hash_password


# Find a user using their email address
def get_user_by_email(db, email):
    user = db.query(User).filter(User.email == email).first()
    return user


"""
db parameter:
- Represents the SQLAlchemy database session.

.first() automatically returns:
- A matching SQLAlchemy User object.
- None if no matching record exists.
"""


"""
Important:
Don't use print() inside the service function.
The router decides what HTTP response to send.

If a user exists, return the user object.
If no user exists, return None.
"""


# Find a user using their database ID
def get_user_by_id(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    return user


# Remember the sequence:
# Receive data → Hash password → Create User object → Add → Commit → Refresh → Return
def create_user(db, user_data):

    # Convert the plain password into a secure hash
    hashed = hash_password(user_data.password)

    # Create a SQLAlchemy User object
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed
    )

    # Add the new user to the database session
    db.add(new_user)

    # Save the changes permanently in the database
    db.commit()

    # Reload database-generated values, such as id and created_at
    db.refresh(new_user)

    return new_user