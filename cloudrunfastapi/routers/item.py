from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4
from sqlmodel import Session

from cloudrunfastapi.database import get_db
from cloudrunfastapi.models import Item, ItemCreate, ItemRead, ItemUpdate, User
from cloudrunfastapi.services.auth import AuthService
from cloudrunfastapi.services.item import item_service

router = APIRouter()
auth_service = AuthService()


@router.post("/items", response_model=ItemRead, tags=["item"])
def create_item(
    current_user: User = Depends(auth_service.current_user),
    item_create: ItemCreate = Body(...),
    db: Session = Depends(get_db),
) -> Item:
    item_create.user_id = current_user.id
    return item_service.create_item(db=db, item_create=item_create)


@router.get("/items/{id}", response_model=ItemRead, tags=["item"])
def get_item(
    id: UUID4,
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> Item:
    item = item_service.get_item(db=db, id=id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item


@router.get("/items", response_model=List[ItemRead], tags=["item"])
def list_items(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> List[Item]:
    items = item_service.list_items(db=db, skip=skip, limit=limit)
    if not items:
        raise HTTPException(status_code=400, detail="Items not found.")
    return items


@router.put("/items/{id}", response_model=ItemRead, tags=["item"])
def update_item(
    id: UUID4,
    current_user: User = Depends(auth_service.current_user),
    item_update: ItemUpdate = Body(...),
    db: Session = Depends(get_db),
) -> Optional[Item]:
    item = item_service.get_user_item(db=db, id=id, user_id=current_user.id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item_service.update_item(db=db, id=id, item_update=item_update)


@router.delete("/items/{id}", response_model=None, tags=["item"])
def delete_item(
    id: UUID4,
    current_user: User = Depends(auth_service.current_user),
    db: Session = Depends(get_db),
) -> None:
    item = item_service.get_user_item(db=db, id=id, user_id=current_user.id)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    return item_service.delete_item(db=db, id=id)
