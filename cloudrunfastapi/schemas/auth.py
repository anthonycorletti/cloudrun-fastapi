from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    id: Optional[UUID4] = None
