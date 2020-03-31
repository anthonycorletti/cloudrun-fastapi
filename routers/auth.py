from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from actions.auth import (authenticate_user, create_access_token,
                          get_current_user)
from config import oauth2_scheme
from database import get_db
from schemas.auth import Token
from schemas.user import User

TOKEN_EXPIRE_MINUTES = 43200

router = APIRouter()


@router.post("/token", response_model=Token, tags=['auth'])
def login_for_access_token(db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/current_user", response_model=User, tags=['auth'])
def current_user(db: Session = Depends(get_db),
                 token: str = Depends(oauth2_scheme)):
    return get_current_user(db, token)
