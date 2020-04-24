import uuid
from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: UUID4) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    db.commit()
    return user


def get_users(db: Session, skip: int, limit: int) -> List[User]:
    users = db.query(User).offset(skip).limit(limit).all()
    db.commit()
    return users


def get_user_by_email(db: Session, user_email: str) -> User:
    user = db.query(User).filter(User.email == user_email).first()
    db.commit()
    return user


def create_user(db: Session, user_create: UserCreate) -> User:
    if get_user_by_email(db, user_create.email):
        raise HTTPException(status_code=422,
                            detail="This email is taken. Try another.")
    user = User(id=str(uuid.uuid4()),
                email=user_create.email,
                name=user_create.name,
                bio=user_create.bio,
                password=user_create.password)
    db.add(user)
    db.commit()
    return user


def update_user(db: Session, user_id: UUID4, user_update: UserUpdate) -> User:
    user = get_user(db, user_id)

    if user.email != user_update.email:
        if get_user_by_email(db, user_update.email):
            raise HTTPException(status_code=422,
                                detail="This email is taken. Try another.")

    for col, val in dict(user_update).items():
        setattr(user, col, val)

    db.commit()
    return user


def delete_user(db: Session, user_id: UUID4):
    user = get_user(db, user_id)

    db.query(User).filter(User.id == user_id).delete()

    db.commit()
    return user
