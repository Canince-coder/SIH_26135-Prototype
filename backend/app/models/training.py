import uuid

from sqlalchemy import String, Text, Integer, Uuid, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TrainingProgram(Base):
    __tablename__ = "training_programs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(200))
    duration: Mapped[str] = mapped_column(String(80))

    skills: Mapped[list["ProgramSkill"]] = relationship(back_populates="program", cascade="all, delete-orphan")


class ProgramSkill(Base):
    __tablename__ = "program_skills"
    __table_args__ = (
        UniqueConstraint("program_id", "skill_id", name="uq_program_skill"),
        CheckConstraint("target_level BETWEEN 1 AND 5", name="ck_target_level_1_5"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    program_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("training_programs.id", ondelete="CASCADE"))
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"))
    target_level: Mapped[int] = mapped_column(Integer)

    program: Mapped["TrainingProgram"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship()  # noqa: F821
