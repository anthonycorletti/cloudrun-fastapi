from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4

from models import User
from tests.v1.factories import ItemFactory
from v1.schemas.item import ItemCreate, ItemORM, ItemUpdate
from v1.services.auth import AuthService
from v1.services.item import ItemService

router = APIRouter()
auth_service = AuthService()
item_service = ItemService()


@router.post("/items", response_model=ItemORM, tags=["item"])
def create_item(current_user: User = Depends(auth_service.current_user),
                item_create: ItemCreate = Body(...,
                                               example=ItemFactory.mock_item)):
    """
    create an item for the current user
    """
    item_create.user_id = current_user.id
    return item_service.create_item(item_create)


@router.get("/items/{id}", response_model=ItemORM, tags=["item"])
def get_item(id: UUID4,
             current_user: User = Depends(auth_service.current_user)):
    """
    get any specific item
    """
    item = item_service.get_item(id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item


@router.get("/items", response_model=List[ItemORM], tags=["item"])
def list_items(skip: int = 0,
               limit: int = 100,
               current_user: User = Depends(auth_service.current_user)):
    """
    get many items
    """
    items = item_service.list_items(skip, limit)
    if not items:
        raise HTTPException(status_code=400, detail="Items not found.")
    return items


@router.put("/items/{id}", response_model=ItemORM, tags=["item"])
def update_item(id: UUID4,
                current_user: User = Depends(auth_service.current_user),
                item_update: ItemUpdate = Body(
                    ..., example=ItemFactory.updated_mock_item)):
    """
    update an item for the current user
    """
    item = item_service.get_user_item(id, current_user.id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item_service.update_item(id, item_update)


@router.delete("/items/{id}", response_model=ItemORM, tags=["item"])
def delete_item(id: UUID4,
                current_user: User = Depends(auth_service.current_user)):
    """
    delete an item for the current user
    """
    item = item_service.get_user_item(id, current_user.id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item_service.delete_item(id)
