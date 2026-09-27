from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.security import require_role
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.trainee import Trainee
from app.models.user import User


def get_current_trainee(
    current_user: User = Depends(require_role(UserRole.TRAINEE)),
    db: Session = Depends(get_db),
) -> Trainee:
    trainee = db.scalar(
        select(Trainee)
        .where(Trainee.user_id == current_user.id)
        .options(selectinload(Trainee.user))
    )
    if trainee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trainee profile not found")
    return trainee
