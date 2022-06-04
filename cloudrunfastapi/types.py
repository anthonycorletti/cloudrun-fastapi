from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr
from pydantic.types import StrictStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    id: Optional[UUID4] = None


class HealthcheckResponse(BaseModel):
    message: StrictStr
    version: StrictStr
    time: datetime
