from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlmodel import Session
from starlette import status

from cloudrunfastapi.database import get_db
from cloudrunfastapi.models import User
from cloudrunfastapi.services.auth import auth_service
from cloudrunfastapi.types import Token

router = APIRouter()


@router.post("/login", response_model=Token, tags=["auth"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = auth_service.authenticate_user(
        db=db, email=EmailStr(form_data.username), password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"id": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=auth_service.TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout", response_model=Token, tags=["auth"])
def logout(current_user: User = Depends(auth_service.current_user)) -> Token:
    return Token(access_token="", token_type="bearer")
