import uuid
from datetime import datetime

from sqlalchemy import String, Text, Uuid, Integer, ForeignKey, DateTime, UniqueConstraint, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)


class TraineeSkill(Base):
    __tablename__ = "trainee_skills"
    __table_args__ = (
        UniqueConstraint("trainee_id", "skill_id", name="uq_trainee_skill"),
        CheckConstraint("proficiency_level BETWEEN 1 AND 5", name="ck_proficiency_1_5"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trainee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trainees.id", ondelete="CASCADE"))
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"))
    proficiency_level: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trainee: Mapped["Trainee"] = relationship(back_populates="skills")  # noqa: F821
    skill: Mapped["Skill"] = relationship()
