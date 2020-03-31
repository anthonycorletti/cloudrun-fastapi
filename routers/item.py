from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from actions import item as item_actions
from database import get_db
from schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.post("/items", response_model=Item, tags=['item'])
def create_item(db: Session = Depends(get_db),
                item: ItemCreate = Body(
                    ...,
                    example={
                        'name': 'Item name',
                        'description': 'Item description'
                    })):
    new_item = item_actions.create_item(db, item)
    return new_item


@router.get('/items/{id}', response_model=Item, tags=['item'])
def get_item(id: UUID4, db: Session = Depends(get_db)):
    item = item_actions.get_item(db, id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item


@router.get('/items', response_model=List[Item], tags=['item'])
def get_items(db: Session = Depends(get_db)):
    items = item_actions.get_items(db)
    if not items:
        raise HTTPException(status_code=400, detail="Items not found.")
    return items


@router.put('/items/{id}', response_model=Item, tags=['item'])
def update_item(id: UUID4,
                db: Session = Depends(get_db),
                new_item: ItemUpdate = Body(
                    ...,
                    example={
                        'name': 'Updated item name',
                        'description': 'Updated item description'
                    })):
    updated_item = item_actions.update_item(db, id, new_item)
    if not updated_item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return updated_item
