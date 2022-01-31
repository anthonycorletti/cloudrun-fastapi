from typing import List

from pydantic import UUID4
from sqlmodel import select

from cloudrunfastapi.database import db_session
from cloudrunfastapi.models import Item, ItemCreate, ItemUpdate


class ItemDAO:
    def get(self, id: UUID4) -> Item:
        with db_session() as db:
            return db.exec(select(Item).where(Item.id == id)).first()

    def get_item_for_user(self, id: UUID4, user_id: UUID4) -> Item:
        with db_session() as db:
            return db.exec(
                select(Item).where(Item.id == id, Item.user_id == user_id)
            ).first()

    def list(self, skip: int, limit: int) -> List[Item]:
        with db_session() as db:
            return db.exec(select(Item).offset(skip).limit(limit)).all()

    def create(self, item_create: ItemCreate) -> Item:
        with db_session() as db:
            item = Item(**item_create.dict())
            db.add(item)
            db.commit()
            db.refresh(item)
        return item

    def update(self, id: UUID4, item_update: ItemUpdate) -> Item:
        # TODO: this does not make use of sqlmodel well
        with db_session() as db:
            db.query(Item).filter(Item.id == id).update(item_update.dict())
            db.commit()
        return self.get(id)

    def delete(self, id: UUID4) -> None:
        with db_session() as db:
            item = db.exec(select(Item).where(Item.id == id)).first()
            db.delete(item)
            db.commit()
        return
