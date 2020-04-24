import uuid
from typing import List

from pydantic import UUID4
from sqlalchemy.orm import Session

from models.item import Item
from schemas.item import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: UUID4) -> Item:
    item = db.query(Item).filter(Item.id == item_id).first()
    db.commit()
    return item


def get_user_item(db: Session, user_id: UUID4, item_id: UUID4) -> Item:
    item = db.query(Item).filter(Item.id == item_id,
                                 Item.user_id == user_id).first()
    db.commit()
    return item


def get_items(db: Session, skip: int, limit: int) -> List[Item]:
    items = db.query(Item).offset(skip).limit(limit).all()
    db.commit()
    return items


def create_item(db: Session, user_id: UUID4, item: ItemCreate) -> Item:
    item = Item(id=str(uuid.uuid4()),
                name=item.name,
                description=item.description,
                user_id=user_id)
    db.add(item)
    db.commit()
    return item


def update_item(db: Session, user_id: UUID4, item_id: UUID4,
                item_update: ItemUpdate) -> Item:
    item = get_user_item(db, user_id, item_id)

    if not item:
        return item

    for col, val in dict(item_update).items():
        setattr(item, col, val)

    db.commit()
    return item


def delete_item(db: Session, user_id: UUID4, item_id: UUID4) -> Item:
    item = get_user_item(db, user_id, item_id)

    if not item:
        return item

    db.query(Item).filter(Item.id == item_id).delete()

    db.commit()
    return item
