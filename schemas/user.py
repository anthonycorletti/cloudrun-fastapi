import string
from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, validator

BIO_CHAR_LIMIT = 160


class UserBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str]

    @validator('bio')
    def bio_length(cls: BaseModel, v: str) -> str:
        if len(v.translate(str.maketrans('', '',
                                         string.whitespace))) > BIO_CHAR_LIMIT:
            raise ValueError(f'bio length must be less than {BIO_CHAR_LIMIT}')
        return v


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    deleted_at: Optional[datetime]


class User(UserBase):
    id: UUID4
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
