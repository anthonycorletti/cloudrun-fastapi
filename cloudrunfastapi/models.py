import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, EmailStr, StrictStr, validator
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

BIO_CHAR_LIMIT = 256


class TimestampsMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )
    )


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, nullable=False)
    name: StrictStr
    bio: Optional[StrictStr]

    @validator("bio", pre=True, always=True)
    def bio_length(cls: BaseModel, v: str) -> str:
        def valid_bio_len(bio: str) -> bool:
            return len(bio) <= BIO_CHAR_LIMIT

        if v is not None and not valid_bio_len(v):
            raise ValueError("Bio is too long.")
        return v


class UserBaseWithPasswordHash(UserBase):
    password_hash: Optional[StrictStr]


class UserCreate(UserBaseWithPasswordHash):
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "Bob Smith",
                "email": "user@example.com",
                "password_hash": "Th3secret_",
                "bio": "logy #puns",
            }
        }


class UserUpdate(UserBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "Robert Smith",
                "email": "new@example.io",
                "bio": "metrics #puns",
            }
        }


class User(UserBaseWithPasswordHash, TimestampsMixin, table=True):
    __tablename__ = "users"
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    items: List["Item"] = Relationship(
        back_populates="user",
    )


class UserRead(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    items: List["Item"]


class ItemBase(SQLModel):
    name: StrictStr
    description: Optional[StrictStr]


class ItemCreate(ItemBase):
    user_id: UUID4

    class Config:
        schema_extra = {
            "example": {
                "name": "A New Item",
                "description": "Many copious details.",
                "user_id": "<UUID4>",
            }
        }


class ItemUpdate(ItemBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "A New New Item",
                "description": "This item has been updated.",
            }
        }


class Item(ItemBase, TimestampsMixin, table=True):
    __tablename__ = "items"
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    user_id: UUID4 = Field(default=None, foreign_key="users.id", nullable=False)
    user: User = Relationship(
        back_populates="items",
    )


class ItemRead(ItemBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
    user: User


UserRead.update_forward_refs()
