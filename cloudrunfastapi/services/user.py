from typing import List, Optional

from pydantic import UUID4, EmailStr
from sqlmodel import Session

from cloudrunfastapi.models import User, UserCreate, UserUpdate


class UserService:
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        user = User(**user_create.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user(self, db: Session, id: UUID4) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_user_by_email(self, db: Session, email: EmailStr) -> Optional[User]:
        return db.query(User).where(User.email == email).first()

    def list_users(self, db: Session, skip: int, limit: int) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def update_user(
        self, db: Session, id: UUID4, user_update: UserUpdate
    ) -> Optional[User]:
        db.query(User).filter(User.id == id).update(user_update.dict())
        db.commit()
        return self.get_user(db=db, id=id)

    def delete_user(self, db: Session, id: UUID4) -> None:
        user = db.query(User).filter(User.id == id).first()
        db.delete(user)
        db.commit()
        return


user_service = UserService()
