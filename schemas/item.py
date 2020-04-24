from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class ItemBase(BaseModel):
    name: str
    description: Optional[str]


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID4
    user_id: UUID4
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
