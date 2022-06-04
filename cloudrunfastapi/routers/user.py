from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4
from sqlmodel import Session

from cloudrunfastapi.database import get_db
from cloudrunfastapi.models import User, UserCreate, UserRead, UserUpdate
from cloudrunfastapi.services.auth import AuthService
from cloudrunfastapi.services.user import user_service

router = APIRouter()
auth_service = AuthService()


@router.post("/users", response_model=UserRead, tags=["user"])
def create_user(
    user_create: UserCreate = Body(...),
    db: Session = Depends(get_db),
) -> User:
    if user_service.get_user_by_email(db=db, email=user_create.email):
        raise HTTPException(status_code=422, detail="This email is taken. Try another.")
    user_create.password_hash = auth_service.create_valid_password_hash(
        data=user_create.password_hash
    )
    return user_service.create_user(db=db, user_create=user_create)


@router.get("/users/{id}", response_model=UserRead, tags=["user"])
def get_user(
    id: UUID4,
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> User:
    user = user_service.get_user(db=db, id=id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    return user


@router.get("/users", response_model=List[UserRead], tags=["user"])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> List[User]:
    return user_service.list_users(db=db, skip=skip, limit=limit)


@router.put("/users", response_model=UserRead, tags=["user"])
def update_user(
    user_update: UserUpdate = Body(...),
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if current_user.email != user_update.email:
        if user_service.get_user_by_email(db=db, email=user_update.email):
            raise HTTPException(
                status_code=422, detail="This email is taken. Try another."
            )
    return user_service.update_user(db=db, id=current_user.id, user_update=user_update)


@router.delete("/users", response_model=None, tags=["user"])
def delete_user(
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> None:
    return user_service.delete_user(db=db, id=current_user.id)
