from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserLogin, Token
from auth import hash_password, verify_password, create_access_token, user_to_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    print("Register request received")
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == data.username.strip()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    # Extract emergency contact safely
    emergency_name = None
    emergency_phone = None

    if data.emergency_contact:
        emergency_name = data.emergency_contact.name
        emergency_phone = data.emergency_contact.number

    # Create user
    user = User(
        username=data.username.strip(),
        password=hash_password(data.password),

        age=data.age,
        gender=data.gender,
        phone_number=data.phone_number.strip() if data.phone_number else None,
        address=data.address.strip() if data.address else None,

        emergency_contact_name=emergency_name,
        emergency_contact_phone=emergency_phone,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate access token
    access_token = create_access_token(user.id)

    return Token(
        access_token=access_token,
        user=user_to_response(user),
    )


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == data.username.strip()).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(user.id)

    return Token(
        access_token=access_token,
        user=user_to_response(user),
    )