from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from pydantic import UUID4, BaseModel, EmailStr, SecretStr, validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BIO_CHAR_LIMIT = 160
PASS_MIN_LENGTH = 8
INVALID_PASS_MSG = (f'Password must be {PASS_MIN_LENGTH} characters or '
                    'more and have a mix of uppercase, lowercase, '
                    'numbers, and special characters.')


def valid_pass(password: str) -> bool:
    valid_length = len(password) >= PASS_MIN_LENGTH
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    special = not password.isalnum()
    return valid_length and upper and lower and special


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def valid_bio_len(bio: str) -> bool:
    return len(bio) <= BIO_CHAR_LIMIT


class UserBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str]

    @validator('bio')
    def bio_length(cls: BaseModel, v: str) -> str:
        if v is not None and not valid_bio_len(v):
            raise ValueError(f'Bio is too long.')
        return v


class UserCreate(UserBase):
    password: SecretStr

    @validator('password')
    def set_valid_password(cls: BaseModel, v: SecretStr) -> str:
        password = v.get_secret_value()
        if not v or not valid_pass(password):
            raise ValueError(INVALID_PASS_MSG)
        return hash_password(password)


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
