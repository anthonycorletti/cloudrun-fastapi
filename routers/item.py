from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4

from actions import auth as auth_actions
from actions import item as item_actions
from config import oauth2_scheme
from schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.post("/items", response_model=Item, tags=['item'])
def create_item(token: str = Depends(oauth2_scheme),
                item_create: ItemCreate = Body(
                    ...,
                    example={
                        'name': 'Item name',
                        'description': 'Item description'
                    })):
    """
    create an item for the current user
    """
    current_user = auth_actions.get_current_user(token)
    item = item_actions.create_item(current_user.id, item_create)
    return item_actions.get_item(item.id)


@router.get('/items/{id}', response_model=Item, tags=['item'])
def get_item(id: UUID4, token: str = Depends(oauth2_scheme)):
    """
    get any specific item
    """
    auth_actions.get_current_user(token)
    item = item_actions.get_item(id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item


@router.get('/items', response_model=List[Item], tags=['item'])
def get_items(skip: int = 0,
              limit: int = 100,
              token: str = Depends(oauth2_scheme)):
    """
    get many items
    """
    auth_actions.get_current_user(token)
    items = item_actions.get_items(skip, limit)
    if not items:
        raise HTTPException(status_code=400, detail="Items not found.")
    return items


@router.put('/items/{id}', response_model=Item, tags=['item'])
def update_item(id: UUID4,
                token: str = Depends(oauth2_scheme),
                item_update: ItemUpdate = Body(
                    ...,
                    example={
                        'name': 'Updated item name',
                        'description': 'Updated item description'
                    })):
    """
    update an item for the current user
    """
    current_user = auth_actions.get_current_user(token)
    item = item_actions.get_user_item(current_user.id, id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item_actions.update_item(current_user.id, id, item_update)


@router.delete('/items/{id}', response_model=Item, tags=['item'])
def delete_item(id: UUID4, token: str = Depends(oauth2_scheme)):
    """
    delete an item for the current user
    """
    current_user = auth_actions.get_current_user(token)
    item = item_actions.get_user_item(current_user.id, id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item_actions.delete_item(item)
