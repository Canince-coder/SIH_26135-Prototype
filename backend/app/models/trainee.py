import uuid
from datetime import datetime

from sqlalchemy import String, Uuid, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Trainee(Base):
    __tablename__ = "trainees"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    district: Mapped[str] = mapped_column(String(120))
    education: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str | None] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="trainee")  # noqa: F821
    skills: Mapped[list["TraineeSkill"]] = relationship(back_populates="trainee", cascade="all, delete-orphan")  # noqa: F821
    applications: Mapped[list["JobApplication"]] = relationship(back_populates="trainee", cascade="all, delete-orphan")  # noqa: F821
    employments: Mapped[list["Employment"]] = relationship(back_populates="trainee", cascade="all, delete-orphan")  # noqa: F821
