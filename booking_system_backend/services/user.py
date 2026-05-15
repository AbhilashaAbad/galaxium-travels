from sqlalchemy.orm import Session
from models import User
from schemas import UserOut, ErrorResponse


def register_user(db: Session, name: str, email: str, seat_preference: str = None) -> UserOut | ErrorResponse:
    """Register a new user with a name and unique email."""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return ErrorResponse(
            error="Email already registered",
            error_code="EMAIL_EXISTS",
            details=f"Email '{email}' is already registered. A user with this email already exists in our system. If you're trying to access an existing account, use get_user with the correct name and email to get the user_id."
        )

    new_user = User(
        name=name,
        email=email,
        frequent_traveller_status='standard',
        seat_preference=seat_preference,
        total_bookings=0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.model_validate(new_user)


def get_user(db: Session, name: str, email: str) -> UserOut | ErrorResponse:
    """Retrieve a user's information by name and email."""
    user = db.query(User).filter(User.name == name, User.email == email).first()
    if not user:
        return ErrorResponse(
            error="User not found",
            error_code="USER_NOT_FOUND",
            details=f"User not found with name '{name}' and email '{email}'. The user may not be registered in our system. Please check the spelling of both name and email, or register the user first."
        )
    return UserOut.model_validate(user)


def update_seat_preference(db: Session, user_id: int, seat_preference: str) -> UserOut | ErrorResponse:
    """Update a user's seat preference (window, aisle, middle)."""
    valid_preferences = ['window', 'aisle', 'middle']
    if seat_preference and seat_preference not in valid_preferences:
        return ErrorResponse(
            error="Invalid seat preference",
            error_code="INVALID_PREFERENCE",
            details=f"Seat preference must be one of: {', '.join(valid_preferences)}. Received: '{seat_preference}'"
        )
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return ErrorResponse(
            error="User not found",
            error_code="USER_NOT_FOUND",
            details=f"User with ID {user_id} not found."
        )
    
    user.seat_preference = seat_preference
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)


def check_and_upgrade_status(db: Session, user_id: int) -> str:
    """Check user's total bookings and upgrade frequent traveller status if eligible.
    
    Status tiers:
    - standard: 0-4 bookings
    - bronze: 5-9 bookings
    - silver: 10-19 bookings
    - gold: 20-49 bookings
    - platinum: 50+ bookings
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return 'standard'
    
    bookings = user.total_bookings
    old_status = user.frequent_traveller_status
    
    if bookings >= 50:
        new_status = 'platinum'
    elif bookings >= 20:
        new_status = 'gold'
    elif bookings >= 10:
        new_status = 'silver'
    elif bookings >= 5:
        new_status = 'bronze'
    else:
        new_status = 'standard'
    
    if new_status != old_status:
        user.frequent_traveller_status = new_status
        db.commit()
    
    return new_status
