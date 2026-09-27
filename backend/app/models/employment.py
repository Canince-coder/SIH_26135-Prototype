import uuid
from datetime import datetime, date

from sqlalchemy import Uuid, ForeignKey, DateTime, Date, Numeric, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Employment(Base):
    __tablename__ = "employments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trainee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trainees.id", ondelete="CASCADE"))
    employer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employers.id", ondelete="CASCADE"))
    job_role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_roles.id", ondelete="CASCADE"))
    job_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("jobs.id", ondelete="SET NULL"))
    joining_date: Mapped[date] = mapped_column(Date)
    salary: Mapped[float | None] = mapped_column(Numeric(12, 2))
    location: Mapped[str] = mapped_column(String(120))
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trainee: Mapped["Trainee"] = relationship(back_populates="employments")  # noqa: F821
    employer: Mapped["Employer"] = relationship()  # noqa: F821
    job_role: Mapped["JobRole"] = relationship()  # noqa: F821
    job: Mapped["Job | None"] = relationship()  # noqa: F821
