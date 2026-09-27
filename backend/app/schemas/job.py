import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.skill import SkillOut


class EmployerBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_name: str
    location: str


class JobRoleBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None = None


class JobRequirementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    skill_id: uuid.UUID
    required_level: int
    required: bool
    skill: SkillOut


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    location: str
    salary_min: float | None = None
    salary_max: float | None = None
    description: str | None = None
    created_at: datetime
    employer: EmployerBrief
    job_role: JobRoleBrief
    requirements: list[JobRequirementOut]


class SkillGapOut(BaseModel):
    skill_id: uuid.UUID
    skill_name: str
    required_level: int
    candidate_level: int
    gap: int
    required: bool


class JobMatchOut(BaseModel):
    job_id: uuid.UUID
    job_title: str
    match_percentage: int
    strengths: list[SkillGapOut]
    skill_gaps: list[SkillGapOut]


class JobSkillGapOut(BaseModel):
    job_id: uuid.UUID
    job_title: str
    match_percentage: int
    skill_gaps: list[SkillGapOut]


class RecommendedJobOut(BaseModel):
    job_id: uuid.UUID
    job: str
    match_percentage: int
    top_skill_gaps: list[str]
    employer: str
    location: str
