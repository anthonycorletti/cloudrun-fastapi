from typing import List

from pydantic import UUID4, EmailStr

from database import db_session
from models import User
from v1.schemas.user import UserCreate, UserUpdate


class UserDAO:
    def get(self, id: UUID4) -> User:
        with db_session() as db:
            return db.query(User).filter(User.id == id).first()

    def list(self, skip: int, limit: int) -> List[User]:
        with db_session() as db:
            return db.query(User).offset(skip).limit(limit).all()

    def get_by_email(self, email: EmailStr) -> User:
        with db_session() as db:
            return db.query(User).filter(User.email == email).first()

    def create(self, user_create: UserCreate) -> User:
        with db_session() as db:
            user = User(**user_create.dict())
            db.add(user)
        return self.get(user.id)

    def update(self, id: UUID4, user_update: UserUpdate) -> User:
        with db_session() as db:
            db.query(User).filter(User.id == id).update(user_update.dict())
        return self.get(id)

    def delete(self, id: UUID4) -> None:
        with db_session() as db:
            db.query(User).filter(User.id == id).delete()
        return
