from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic identity
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    # Demographics & contact
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    phone_number = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)

    # Patient-specific
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)

    # Psychiatrist-specific (future / optional)
    degree_info = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def name_for_profile(self) -> str:
        # The project currently stores only `username`; we treat it as the profile name.
        return self.username
