from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import UUID4
from starlette import status

from actions.user import get_user, get_user_by_email
from config import apisecrets, get_logger, oauth2_scheme
from models.user import User
from schemas.auth import TokenData

logger = get_logger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = apisecrets.SECRET_KEY
ACCESS_TOKEN_ALGORITHM = 'HS256'
credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Invalid credentials.",
                                      headers={"WWW-Authenticate": "Bearer"})


def valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user_email: UUID4, password: str) -> Union[bool, User]:
    user = get_user_by_email(user_email)
    if not user:
        return False
    if not valid_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta) -> bytes:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY,
                             algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ACCESS_TOKEN_ALGORITHM])
        id, email = payload.get("id"), payload.get("email")
        if email is None or email == '':
            raise credentials_exception
        token_data = TokenData(id=id, email=email)
    except PyJWTError:
        raise credentials_exception
    user = get_user(token_data.id)
    if user is None:
        raise credentials_exception
    return user
