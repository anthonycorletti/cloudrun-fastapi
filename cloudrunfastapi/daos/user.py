from typing import List

from pydantic import UUID4, EmailStr
from sqlmodel import select

from cloudrunfastapi.database import db_session
from cloudrunfastapi.models import User, UserCreate, UserUpdate


class UserDAO:
    def get(self, id: UUID4) -> User:
        with db_session() as db:
            return db.exec(select(User).where(User.id == id)).first()

    def list(self, skip: int, limit: int) -> List[User]:
        with db_session() as db:
            return db.exec(select(User).offset(skip).limit(limit)).all()

    def get_by_email(self, email: EmailStr) -> User:
        with db_session() as db:
            return db.exec(select(User).where(User.email == email)).first()

    def create(self, user_create: UserCreate) -> User:
        with db_session() as db:
            user = User(**user_create.dict())
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def update(self, id: UUID4, user_update: UserUpdate) -> User:
        # TODO: this does not make use of sqlmodel well
        with db_session() as db:
            db.query(User).filter(User.id == id).update(user_update.dict())
            db.commit()
        return self.get(id)

    def delete(self, id: UUID4) -> None:
        with db_session() as db:
            user = db.exec(select(User).where(User.id == id)).first()
            db.delete(user)
            db.commit()
        return
