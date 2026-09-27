import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skill import TraineeSkill


@dataclass
class SkillMatch:
    skill_id: uuid.UUID
    skill_name: str
    required_level: int
    candidate_level: int
    gap: int
    required: bool
    score: float


@dataclass
class MatchResult:
    match_percentage: float
    per_skill: list[SkillMatch]

    @property
    def strengths(self) -> list[SkillMatch]:
        return [s for s in self.per_skill if s.gap == 0]

    @property
    def gaps(self) -> list[SkillMatch]:
        return sorted(
            (s for s in self.per_skill if s.gap > 0),
            key=lambda s: (-s.gap, s.skill_name),
        )


def load_trainee_skill_levels(db: Session, trainee_id: uuid.UUID) -> dict[uuid.UUID, int]:
    rows = db.execute(
        select(TraineeSkill.skill_id, TraineeSkill.proficiency_level).where(
            TraineeSkill.trainee_id == trainee_id
        )
    ).all()
    return {skill_id: int(level) for skill_id, level in rows}


def compute_match(
    skill_levels: dict[uuid.UUID, int],
    requirements,
) -> MatchResult:
    """Transparent scoring per the brief.

    For each job requirement:
        score = min(candidate_level / required_level, 1)
        gap   = max(0, required_level - candidate_level)
    match_percentage = average(score) * 100  (0.0 when the job has no requirements)
    A skill the trainee does not have counts as candidate_level 0.
    """
    per_skill: list[SkillMatch] = []
    total = 0.0
    for rq in requirements:
        candidate = int(skill_levels.get(rq.skill_id, 0))
        required_level = int(rq.required_level)
        score = min(candidate / required_level, 1.0) if required_level > 0 else 1.0
        total += score
        gap = max(0, required_level - candidate)
        per_skill.append(
            SkillMatch(
                skill_id=rq.skill_id,
                skill_name=rq.skill.name if rq.skill is not None else "",
                required_level=required_level,
                candidate_level=candidate,
                gap=gap,
                required=bool(rq.required),
                score=score,
            )
        )
    match_percentage = (total / len(per_skill) * 100.0) if per_skill else 0.0
    return MatchResult(match_percentage=match_percentage, per_skill=per_skill)
