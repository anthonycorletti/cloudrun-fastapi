from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from models import User
from v1.schemas.auth import Token
from v1.services.auth import AuthService

TOKEN_EXPIRE_MINUTES = 43200

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=Token, tags=['auth'])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(form_data.username,
                                          form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={
            "id": str(user.id),
            "email": user.email
        },
        expires_delta=timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout", response_model=Token, tags=["auth"])
def logout(current_user: User = Depends(auth_service.current_user)):
    """
    return an empty token, assuming login and logout
    workflows are handled in a client
    """
    return Token(access_token="", token_type="bearer")
