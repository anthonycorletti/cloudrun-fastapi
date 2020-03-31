import uuid
from datetime import datetime

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from models.item import Item
from schemas.item import ItemCreate, ItemDelete, ItemUpdate


def get_item(db: Session, item_id: UUID4):
    return db.query(Item).filter(Item.id == item_id,
                                 Item.deleted_at.is_(None)).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).filter(
        Item.deleted_at.is_(None)).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(id=str(uuid.uuid4()),
                   name=item.name,
                   description=item.description,
                   user_id=item.user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: UUID4, item_update: ItemUpdate):
    item = get_item(db, item_id)

    if not item:
        return item

    if item.user_id != item_update.user_id:
        raise HTTPException(status_code=401, detail='Cannot update this item.')

    for col, val in dict(item_update).items():
        setattr(item, col, val)

    db.commit()
    return get_item(db, item_id)


def delete_item(db: Session, item_id: UUID4, item_delete: ItemDelete):
    item = get_item(db, item_id)

    if not item:
        return item

    if item.user_id != item_delete.user_id:
        raise HTTPException(status_code=401, detail='Cannot delete this item.')

    for col, val in dict(item_delete).items():
        setattr(item, col, val)

    db.commit()
    return item
