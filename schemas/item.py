from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class ItemBase(BaseModel):
    name: str
    description: Optional[str]
    user_id: Optional[UUID4]


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemDelete(BaseModel):
    deleted_at: datetime
    user_id: Optional[UUID4]


class Item(ItemBase):
    id: UUID4
    user_id: UUID4
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
