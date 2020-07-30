from pydantic import UUID4, BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr = None
    id: UUID4 = None
