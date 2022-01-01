from typing import List

from pydantic import UUID4

from cloudrunfastapi.daos.item import ItemDAO
from cloudrunfastapi.schemas.item import ItemCreate, ItemUpdate
from models import Item

item_dao = ItemDAO()


class ItemService:
    def create_item(self, item_create: ItemCreate) -> Item:
        return item_dao.create(item_create)

    def get_item(self, id: UUID4) -> Item:
        return item_dao.get(id)

    def list_items(self, skip: int, limit: int) -> List[Item]:
        return item_dao.list(skip, limit)

    def get_user_item(self, id: UUID4, user_id: UUID4) -> Item:
        return item_dao.get_by_user(id, user_id)

    def update_item(self, id: UUID4, item_update: ItemUpdate) -> Item:
        return item_dao.update(id, item_update)

    def delete_item(self, id: UUID4) -> None:
        return item_dao.delete(id)
