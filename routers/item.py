from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from actions import auth as auth_actions
from actions import item as item_actions
from config import oauth2_scheme
from database import get_db
from schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.post("/items", response_model=Item, tags=['item'])
def create_item(db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme),
                item: ItemCreate = Body(
                    ...,
                    example={
                        'name': 'Item name',
                        'description': 'Item description'
                    })):
    current_user = auth_actions.get_current_user(db, token)
    item.user_id = current_user.id
    new_item = item_actions.create_item(db, item)
    return new_item


@router.get('/items/{id}', response_model=Item, tags=['item'])
def get_item(id: UUID4,
             db: Session = Depends(get_db),
             token: str = Depends(oauth2_scheme)):
    item = item_actions.get_item(db, id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item


@router.get('/items', response_model=List[Item], tags=['item'])
def get_items(db: Session = Depends(get_db),
              token: str = Depends(oauth2_scheme)):
    items = item_actions.get_items(db)
    if not items:
        raise HTTPException(status_code=400, detail="Items not found.")
    return items


@router.put('/items/{id}', response_model=Item, tags=['item'])
def update_item(id: UUID4,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme),
                new_item: ItemUpdate = Body(
                    ...,
                    example={
                        'name': 'Updated item name',
                        'description': 'Updated item description'
                    })):
    current_user = auth_actions.get_current_user(db, token)
    if current_user.id != id:
        raise HTTPException(status_code=401)
    updated_item = item_actions.update_item(db, id, new_item)
    if not updated_item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return updated_item


@router.delete('/items/{id}', response_model=Item, tags=['item'])
def delete_item(id: UUID4,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    current_user = auth_actions.get_current_user(db, token)
    if current_user.id != id:
        raise HTTPException(status_code=401)
    deleted_item = item_actions.delete_item(db, id)
    if not deleted_item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return deleted_item
