from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Basic identity
    name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # "patient" or "psychiatrist"

    # Demographics & contact
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    phone_number = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)

    # Patient-specific
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)

    # Psychiatrist-specific
    degree_info = Column(Text, nullable=True)  # e.g. degree name / registration number / link

    created_at = Column(DateTime(timezone=True), server_default=func.now())
