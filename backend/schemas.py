from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field


class EmergencyContact(BaseModel):
    name: str
    number: str


class UserCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)

    age: int | None = None
    gender: str | None = None
    phone_number: str | None = None
    address: str | None = None

    emergency_contact: Optional[EmergencyContact] = None


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: int
    
    username: str
    
    created_at: str | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ChatMessageCreate(BaseModel):
    text: Optional[str] = None
    mic_on: bool = False
    camera_on: bool = False
    session_id: str


class ChatMessageResponse(BaseModel):
    reply: str
