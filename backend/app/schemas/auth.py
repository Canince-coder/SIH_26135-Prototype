import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserRole


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.TRAINEE
    # optional profile fields, used to auto-provision the role-specific record
    district: str | None = Field(default=None, max_length=120)
    education: str | None = Field(default=None, max_length=200)
    phone: str | None = Field(default=None, max_length=20)
    company_name: str | None = Field(default=None, max_length=200)
    location: str | None = Field(default=None, max_length=120)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
