from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4

from cloudrunfastapi.models import User, UserCreate, UserDB, UserUpdate
from cloudrunfastapi.services.auth import AuthService
from cloudrunfastapi.services.user import UserService

router = APIRouter()
auth_service = AuthService()
user_service = UserService()


@router.post("/users", response_model=UserDB, tags=["user"])
def create_user(
    user_create: UserCreate = Body(...),
) -> User:
    if user_service.get_user_by_email(user_create.email):
        raise HTTPException(status_code=422, detail="This email is taken. Try another.")
    user_create.password_hash = auth_service.create_valid_password_hash(
        data=user_create.password_hash
    )
    return user_service.create_user(user_create)


@router.get("/users/{id}", response_model=UserDB, tags=["user"])
def get_user(
    id: UUID4, current_user: User = Depends(auth_service.current_user)
) -> User:
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    return user


@router.get("/users", response_model=List[UserDB], tags=["user"])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth_service.current_user),
) -> List[User]:
    return user_service.list_users(skip, limit)


@router.put("/users", response_model=UserDB, tags=["user"])
def update_user(
    current_user: User = Depends(auth_service.current_user),
    user_update: UserUpdate = Body(...),
) -> User:
    if current_user.email != user_update.email:
        if user_service.get_user_by_email(user_update.email):
            raise HTTPException(
                status_code=422, detail="This email is taken. Try another."
            )
    return user_service.update_user(current_user.id, user_update)


@router.delete("/users", response_model=None, tags=["user"])
def delete_user(current_user: User = Depends(auth_service.current_user)) -> None:
    return user_service.delete_user(current_user.id)
