import uuid
from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status

from cloudrunfastapi.apienv import apienv
from cloudrunfastapi.services.user import UserService
from models import User

user_service = UserService()
oauth2_scheme_pwdbearer_route = "/login"
oauth2_scheme_pwdbearer = OAuth2PasswordBearer(tokenUrl=oauth2_scheme_pwdbearer_route)
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
API_SECRET_KEY = apienv.API_SECRET_KEY
ACCESS_TOKEN_ALGORITHM = "HS256"
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthService:
    def valid_password(self, plain_pass: str, hashed_pass: str) -> bool:
        return PWD_CONTEXT.verify(plain_pass, hashed_pass)

    def authenticate_user(self, email: EmailStr, password: str) -> Union[None, User]:
        user = user_service.get_user_by_email(email)
        if not user:
            return None
        if not self.valid_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, API_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM
        )
        return encoded_jwt

    def current_user(self, token: str = Depends(oauth2_scheme_pwdbearer)) -> User:
        try:
            payload = jwt.decode(
                token, API_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
            )
            id = payload["id"]
        except PyJWTError:
            raise CREDENTIALS_EXCEPTION
        return user_service.get_user(uuid.UUID(id))
