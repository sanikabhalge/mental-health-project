from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Common fields
    name: str = Field(..., min_length=1, max_length=255)
    username: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)
    role: Literal["patient", "psychiatrist"]

    age: int | None = None
    gender: str | None = None
    phone_number: str | None = Field(None, alias="phoneNumber")
    address: str | None = None

    # Patient-specific
    emergency_contact_name: str | None = Field(None, alias="emergencyContactName")
    emergency_contact_phone: str | None = Field(None, alias="emergencyContactPhone")

    # Psychiatrist-specific
    degree_info: str | None = Field(None, alias="degreeInfo")


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    role: str
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
