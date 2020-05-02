import uuid
from typing import List

from pydantic import UUID4

from database import db_session
from models.user import User
from schemas.user import UserCreate, UserUpdate


def get_user(user_id: UUID4) -> User:
    with db_session() as db:
        return db.query(User).filter(User.id == user_id).first()


def get_users(skip: int, limit: int) -> List[User]:
    with db_session() as db:
        return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(user_email: str) -> User:
    with db_session() as db:
        return db.query(User).filter(User.email == user_email).first()


def create_user(user_create: UserCreate) -> User:
    with db_session() as db:
        user = User(id=str(uuid.uuid4()),
                    email=user_create.email,
                    name=user_create.name,
                    bio=user_create.bio,
                    password=user_create.password)
        db.add(user)
        return user


def update_user(user_id: UUID4, user_update: UserUpdate) -> User:
    with db_session() as db:
        db.query(User).filter(User.id == user_id).update(user_update.dict())
    return get_user(user_id)


def delete_user(user: User) -> User:
    with db_session() as db:
        db.query(User).filter(User.id == user.id).delete()
    return user
