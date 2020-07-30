from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4

from models import User
from tests.v1.factories import UserFactory
from v1.schemas.user import UserCreate, UserORM, UserUpdate
from v1.services.auth import AuthService
from v1.services.user import UserService

router = APIRouter()
auth_service = AuthService()
user_service = UserService()


@router.post("/users", response_model=UserORM, tags=["user"])
def create_user(
        user_create: UserCreate = Body(...,
                                       example=UserFactory.mock_user_bob), ):
    """
    create a new user
    """
    if user_service.get_user_by_email(user_create.email):
        raise HTTPException(status_code=422,
                            detail="This email is taken. Try another.")
    return user_service.create_user(user_create)


@router.get("/users/{id}", response_model=UserORM, tags=["user"])
def get_user(id: UUID4,
             current_user: User = Depends(auth_service.current_user)):
    """
    get any user
    """
    user = user_service.get_user(id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    return user


@router.get("/users", response_model=List[UserORM], tags=["user"])
def list_users(skip: int = 0,
               limit: int = 100,
               current_user: User = Depends(auth_service.current_user)):
    """
    get many users
    """
    return user_service.list_users(skip, limit)


@router.put("/users", response_model=UserORM, tags=["user"])
def update_user(current_user: User = Depends(auth_service.current_user),
                user_update: UserUpdate = Body(
                    ..., example=UserFactory.mock_user_bob_update)):
    """
    update the current user
    """

    if current_user.email != user_update.email:
        if user_service.get_user_by_email(user_update.email):
            raise HTTPException(status_code=422,
                                detail="This email is taken. Try another.")
    return user_service.update_user(current_user.id, user_update)


@router.delete("/users", tags=["user"])
def delete_user(current_user: User = Depends(auth_service.current_user)):
    """
    delete the current user
    """
    return user_service.delete_user(current_user.id)
