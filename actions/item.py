import uuid
from typing import List

from pydantic import UUID4

from database import db_session
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate


def get_item(item_id: UUID4) -> Item:
    with db_session() as db:
        return db.query(Item).filter(Item.id == item_id).first()


def get_user_item(user_id: UUID4, item_id: UUID4) -> Item:
    with db_session() as db:
        return db.query(Item).filter(Item.id == item_id,
                                     Item.user_id == user_id).first()


def get_items(skip: int, limit: int) -> List[Item]:
    with db_session() as db:
        return db.query(Item).offset(skip).limit(limit).all()


def create_item(user_id: UUID4, item: ItemCreate) -> Item:
    with db_session() as db:
        item = Item(id=str(uuid.uuid4()),
                    name=item.name,
                    description=item.description,
                    user_id=user_id)
        db.add(item)
        return item


def update_item(user_id: UUID4, id: UUID4, item_update: ItemUpdate) -> Item:
    with db_session() as db:
        db.query(Item).filter(Item.id == id, Item.user_id == user_id).update(
            item_update.dict())
    return get_item(id)


def delete_item(item: Item) -> Item:
    with db_session() as db:
        db.query(Item).filter(Item.id == item.id).delete()
    return item
