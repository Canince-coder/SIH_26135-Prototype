from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.deps import get_current_trainee
from app.db.session import get_db
from app.models.job import Job, JobRequirement
from app.models.skill import Skill, TraineeSkill
from app.models.trainee import Trainee
from app.schemas.job import RecommendedJobOut
from app.schemas.skill import TraineeSkillCreate, TraineeSkillOut
from app.schemas.trainee import TraineeOut, TraineeUpdate
from app.services.matching import compute_match, load_trainee_skill_levels

router = APIRouter(prefix="/trainees", tags=["trainees"])

TOP_GAPS = 3


@router.get("/me", response_model=TraineeOut)
def read_my_profile(trainee: Trainee = Depends(get_current_trainee)):
    return trainee


@router.put("/me", response_model=TraineeOut)
def update_my_profile(
    payload: TraineeUpdate,
    trainee: Trainee = Depends(get_current_trainee),
    db: Session = Depends(get_db),
):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(trainee, field, value)
    db.commit()
    db.refresh(trainee)
    return trainee


@router.get("/me/skills", response_model=list[TraineeSkillOut])
def list_my_skills(
    trainee: Trainee = Depends(get_current_trainee),
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(TraineeSkill)
        .where(TraineeSkill.trainee_id == trainee.id)
        .options(selectinload(TraineeSkill.skill))
        .order_by(TraineeSkill.created_at)
    ).all()
    return rows


@router.post("/me/skills", response_model=TraineeSkillOut, status_code=status.HTTP_201_CREATED)
def add_my_skill(
    payload: TraineeSkillCreate,
    trainee: Trainee = Depends(get_current_trainee),
    db: Session = Depends(get_db),
):
    skill = db.get(Skill, payload.skill_id)
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")

    already = db.scalar(
        select(TraineeSkill).where(
            TraineeSkill.trainee_id == trainee.id,
            TraineeSkill.skill_id == payload.skill_id,
        )
    )
    if already is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill already added for this trainee",
        )

    trainee_skill = TraineeSkill(
        trainee_id=trainee.id,
        skill_id=payload.skill_id,
        proficiency_level=payload.proficiency_level,
    )
    db.add(trainee_skill)
    db.commit()
    db.refresh(trainee_skill)
    return trainee_skill


@router.get("/me/recommended-jobs", response_model=list[RecommendedJobOut])
def recommended_jobs(
    limit: int = Query(10, ge=1, le=50),
    trainee: Trainee = Depends(get_current_trainee),
    db: Session = Depends(get_db),
):
    levels = load_trainee_skill_levels(db, trainee.id)
    jobs = db.scalars(
        select(Job).options(
            selectinload(Job.employer),
            selectinload(Job.requirements).selectinload(JobRequirement.skill),
        )
    ).all()

    ranked = []
    for job in jobs:
        result = compute_match(levels, job.requirements)
        top_gaps = [s.skill_name for s in result.gaps][:TOP_GAPS]
        ranked.append((result.match_percentage, job, top_gaps))

    ranked.sort(key=lambda item: (-item[0], item[1].title))

    return [
        RecommendedJobOut(
            job_id=job.id,
            job=job.title,
            match_percentage=round(pct),
            top_skill_gaps=top_gaps,
            employer=job.employer.company_name,
            location=job.location,
        )
        for pct, job, top_gaps in ranked[:limit]
    ]
