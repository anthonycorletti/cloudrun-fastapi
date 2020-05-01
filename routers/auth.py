from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from actions.auth import (authenticate_user, create_access_token,
                          get_current_user)
from config import oauth2_scheme
from schemas.auth import Token
from schemas.user import User

TOKEN_EXPIRE_MINUTES = 43200

router = APIRouter()


@router.post("/login", response_model=Token, tags=['auth'])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {'id': str(user.id), 'email': user.email}
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=data,
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", response_model=Token, tags=['auth'])
def logout(token: str = Depends(oauth2_scheme)):
    '''
    return an invalid token, assuming login and logout
    workflows are handled in a client
    '''
    current_user = get_current_user(token)
    access_token_expires = timedelta(minutes=-1)
    data = {'id': str(current_user.id), 'email': current_user.email}
    expired_token = create_access_token(data=data,
                                        expires_delta=access_token_expires)
    return {"access_token": expired_token, "token_type": "bearer"}


@router.get("/current_user", response_model=User, tags=['auth'])
def current_user(token: str = Depends(oauth2_scheme)):
    return get_current_user(token)
