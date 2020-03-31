import uuid
from datetime import datetime

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from config import get_logger
from models.user import User
from schemas.user import UserCreate, UserUpdate

logger = get_logger()


def get_user(db: Session, user_id: UUID4):
    return db.query(User).filter(User.id == user_id,
                                 User.deleted_at.is_(None)).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email,
                                 User.deleted_at.is_(None)).first()


def create_user(db: Session, user: UserCreate):
    id = str(uuid.uuid4())

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail='An account already exists with this email.')

    db_user = User(id=id,
                   email=user.email,
                   name=user.name,
                   bio=user.bio,
                   password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: UUID4, user_update: UserUpdate):
    user = get_user(db, user_id)

    if not user:
        return user

    for col, val in dict(user_update).items():
        setattr(user, col, val)

    db.commit()
    return get_user(db, user_id)


def delete_user(db: Session, user_id: UUID4):
    user = get_user(db, user_id)

    if not user:
        return user

    setattr(user, 'deleted_at', datetime.now())

    db.commit()
    return user
