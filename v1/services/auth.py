from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status

from config import apisecrets, oauth2_scheme
from models import User
from v1.services.user import UserService

user_service = UserService()
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = apisecrets.SECRET_KEY
ACCESS_TOKEN_ALGORITHM = 'HS256'
CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Invalid credentials.",
                                      headers={"WWW-Authenticate": "Bearer"})


class AuthService:
    def valid_password(self, plain_pass: str, hashed_pass: str) -> bool:
        return PWD_CONTEXT.verify(plain_pass, hashed_pass)

    def authenticate_user(self, email: EmailStr, password: str) -> User:
        user = user_service.get_user_by_email(email)
        if not user:
            return
        if not self.valid_password(password, user.password):
            return
        return user

    def create_access_token(self, data: dict,
                            expires_delta: timedelta) -> bytes:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode,
                                 SECRET_KEY,
                                 algorithm=ACCESS_TOKEN_ALGORITHM)
        return encoded_jwt

    def current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        try:
            payload = jwt.decode(token,
                                 SECRET_KEY,
                                 algorithms=[ACCESS_TOKEN_ALGORITHM])
            id = payload.get("id")
        except PyJWTError:
            raise CREDENTIALS_EXCEPTION
        return user_service.get_user(id)
