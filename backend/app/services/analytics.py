import uuid
from dataclasses import dataclass, field
 
from sqlalchemy import func, select
from sqlalchemy.orm import Session
 
from app.models.application import JobApplication
from app.models.employer import Employer
from app.models.employment import Employment
from app.models.enums import ApplicationStatus
from app.models.job import Job, JobRequirement
from app.models.skill import Skill, TraineeSkill
from app.models.trainee import Trainee
 
 
@dataclass
class PlatformOverview:
    total_trainees: int
    total_employers: int
    total_jobs: int
    total_skills: int
    total_applications: int
    total_employments: int
    employed_trainees: int
    employment_rate: float  # percentage, 0.0 when there are no trainees
 
 
@dataclass
class SkillDemandSupply:
    skill_id: uuid.UUID
    skill_name: str
    demand_count: int  # how many job_requirements reference this skill
    supply_count: int  # how many trainees hold this skill
    gap: int  # demand_count - supply_count
 
 
@dataclass
class EmployerAnalytics:
    total_jobs: int
    total_applications: int
    applications_by_status: dict[ApplicationStatus, int]
    total_employments: int
 
 
_ALL_STATUSES = list(ApplicationStatus)
 
 
def get_platform_overview(db: Session) -> PlatformOverview:
    total_trainees = db.scalar(select(func.count()).select_from(Trainee)) or 0
    total_employers = db.scalar(select(func.count()).select_from(Employer)) or 0
    total_jobs = db.scalar(select(func.count()).select_from(Job)) or 0
    total_skills = db.scalar(select(func.count()).select_from(Skill)) or 0
    total_applications = db.scalar(select(func.count()).select_from(JobApplication)) or 0
    total_employments = db.scalar(select(func.count()).select_from(Employment)) or 0
    employed_trainees = db.scalar(
        select(func.count(func.distinct(Employment.trainee_id)))
    ) or 0
    employment_rate = (employed_trainees / total_trainees * 100.0) if total_trainees else 0.0
 
    return PlatformOverview(
        total_trainees=total_trainees,
        total_employers=total_employers,
        total_jobs=total_jobs,
        total_skills=total_skills,
        total_applications=total_applications,
        total_employments=total_employments,
        employed_trainees=employed_trainees,
        employment_rate=employment_rate,
    )
 
 
def get_applications_by_status(db: Session) -> dict[ApplicationStatus, int]:
    rows = db.execute(
        select(JobApplication.status, func.count()).group_by(JobApplication.status)
    ).all()
    counts = {status: 0 for status in _ALL_STATUSES}
    for status, count in rows:
        counts[status] = count
    return counts
 
 
def get_skills_demand_supply(db: Session, limit: int = 10) -> list[SkillDemandSupply]:
    demand_rows = db.execute(
        select(JobRequirement.skill_id, func.count(JobRequirement.id)).group_by(JobRequirement.skill_id)
    ).all()
    demand = {skill_id: count for skill_id, count in demand_rows}
 
    supply_rows = db.execute(
        select(TraineeSkill.skill_id, func.count(TraineeSkill.id)).group_by(TraineeSkill.skill_id)
    ).all()
    supply = {skill_id: count for skill_id, count in supply_rows}
 
    skills = db.execute(select(Skill.id, Skill.name)).all()
 
    results = [
        SkillDemandSupply(
            skill_id=skill_id,
            skill_name=name,
            demand_count=demand.get(skill_id, 0),
            supply_count=supply.get(skill_id, 0),
            gap=demand.get(skill_id, 0) - supply.get(skill_id, 0),
        )
        for skill_id, name in skills
    ]
    results.sort(key=lambda r: (-r.gap, -r.demand_count, r.skill_name))
    return results[:limit]
 
 
def get_employer_analytics(db: Session, employer_id: uuid.UUID) -> EmployerAnalytics:
    total_jobs = db.scalar(
        select(func.count()).select_from(Job).where(Job.employer_id == employer_id)
    ) or 0
 
    total_applications = db.scalar(
        select(func.count())
        .select_from(JobApplication)
        .join(Job, JobApplication.job_id == Job.id)
        .where(Job.employer_id == employer_id)
    ) or 0
 
    status_rows = db.execute(
        select(JobApplication.status, func.count())
        .join(Job, JobApplication.job_id == Job.id)
        .where(Job.employer_id == employer_id)
        .group_by(JobApplication.status)
    ).all()
    applications_by_status = {status: 0 for status in _ALL_STATUSES}
    for status, count in status_rows:
        applications_by_status[status] = count
 
    total_employments = db.scalar(
        select(func.count()).select_from(Employment).where(Employment.employer_id == employer_id)
    ) or 0
 
    return EmployerAnalytics(
        total_jobs=total_jobs,
        total_applications=total_applications,
        applications_by_status=applications_by_status,
        total_employments=total_employments,
    )