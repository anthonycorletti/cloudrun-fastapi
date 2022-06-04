from typing import List, Optional

from pydantic import UUID4
from sqlmodel import Session

from cloudrunfastapi.models import Item, ItemCreate, ItemUpdate


class ItemService:
    def create_item(self, db: Session, item_create: ItemCreate) -> Item:
        item = Item(**item_create.dict())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_item(self, db: Session, id: UUID4) -> Optional[Item]:
        return db.query(Item).filter(Item.id == id).first()

    def list_items(self, db: Session, skip: int, limit: int) -> List[Item]:
        return db.query(Item).offset(skip).limit(limit).all()

    def get_user_item(self, db: Session, id: UUID4, user_id: UUID4) -> Optional[Item]:
        return db.query(Item).filter(Item.id == id, Item.user_id == user_id).first()

    def update_item(
        self, db: Session, id: UUID4, item_update: ItemUpdate
    ) -> Optional[Item]:
        db.query(Item).filter(Item.id == id).update(item_update.dict())
        db.commit()
        return self.get_item(db=db, id=id)

    def delete_item(self, db: Session, id: UUID4) -> None:
        item = db.query(Item).filter(Item.id == id).first()
        db.delete(item)
        db.commit()
        return


item_service = ItemService()
