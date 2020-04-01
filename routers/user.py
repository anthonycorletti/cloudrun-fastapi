from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from actions import auth as auth_actions
from actions import user as user_actions
from config import get_logger, oauth2_scheme
from database import get_db
from schemas.user import User, UserCreate, UserDelete, UserUpdate

router = APIRouter()

logger = get_logger()


@router.post("/users", response_model=User, tags=['user'])
def create_user(db: Session = Depends(get_db),
                user: UserCreate = Body(
                    ...,
                    example={
                        'name': 'Bob',
                        'email': 'bob@example.com',
                        'password': 'Thes3cret_'
                    })):
    new_user = user_actions.create_user(db, user)
    return new_user


@router.get('/users/{id}', response_model=User, tags=['user'])
def get_user(id: UUID4,
             db: Session = Depends(get_db),
             token: str = Depends(oauth2_scheme)):
    user = user_actions.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.put('/users/{id}', response_model=User, tags=['user'])
def update_user(id: UUID4,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme),
                new_user: UserUpdate = Body(
                    ...,
                    example={
                        'name': 'Robert',
                        'email': 'bob@example.com',
                        'bio': 'logy #puns'
                    })):
    current_user = auth_actions.get_current_user(db, token)
    if current_user.id != id:
        raise HTTPException(status_code=401)
    updated_user = user_actions.update_user(db, id, new_user)
    return updated_user


@router.delete('/users/{id}', tags=['user'])
def delete_user(id: UUID4,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme),
                user_delete: UserDelete = Body(
                    ..., example={'deleted_at': str(datetime.now())})):
    current_user = auth_actions.get_current_user(db, token)
    if current_user.id != id:
        raise HTTPException(status_code=401)
    deleted_user = user_actions.delete_user(db, id, user_delete)
    return deleted_user
