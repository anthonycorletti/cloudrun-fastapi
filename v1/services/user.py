from typing import List

from pydantic import UUID4, EmailStr

from models import User
from v1.daos.user import UserDAO
from v1.schemas.user import UserCreate, UserUpdate

user_dao = UserDAO()


class UserService:
    def create_user(self, user_create: UserCreate) -> User:
        return user_dao.create(user_create)

    def get_user(self, id: UUID4) -> User:
        return user_dao.get(id)

    def get_user_by_email(self, email: EmailStr) -> User:
        return user_dao.get_by_email(email)

    def list_users(self, skip: int, limit: int) -> List[User]:
        return user_dao.list(skip, limit)

    def update_user(self, id: UUID4, user_update: UserUpdate) -> User:
        return user_dao.update(id, user_update)

    def delete_user(self, id: UUID4) -> None:
        return user_dao.delete(id)
