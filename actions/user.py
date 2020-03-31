import uuid

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: UUID4):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    id = str(uuid.uuid4())
    db_user = User(id=id, email=user.email, name=user.name, bio=user.bio)
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
