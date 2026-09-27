import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None = None


class TraineeSkillCreate(BaseModel):
    skill_id: uuid.UUID
    proficiency_level: int = Field(ge=1, le=5)


class TraineeSkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    skill_id: uuid.UUID
    proficiency_level: int
    created_at: datetime
    skill: SkillOut
