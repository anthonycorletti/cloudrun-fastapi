from pydantic import UUID4, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    id: UUID4 = None
