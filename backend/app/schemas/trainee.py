import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TraineeUserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: EmailStr


class TraineeUpdate(BaseModel):
    district: str | None = Field(default=None, max_length=120)
    education: str | None = Field(default=None, max_length=200)
    phone: str | None = Field(default=None, max_length=20)


class TraineeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    district: str
    education: str
    phone: str | None = None
    created_at: datetime
    user: TraineeUserOut
