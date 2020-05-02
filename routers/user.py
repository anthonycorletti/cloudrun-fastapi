from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import UUID4

from actions import auth as auth_actions
from actions import user as user_actions
from config import oauth2_scheme
from schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.post("/users", response_model=User, tags=['user'])
def create_user(user_create: UserCreate = Body(
    ...,
    example={
        'name': 'Bob',
        'email': 'bob@example.com',
        'password': 'Thes3cret_'
    },
)):
    """
    create a new user
    """
    if user_actions.get_user_by_email(user_create.email):
        raise HTTPException(status_code=422,
                            detail="This email is taken. Try another.")
    user = user_actions.create_user(user_create)
    return user_actions.get_user(user.id)


@router.get('/users/{id}', response_model=User, tags=['user'])
def get_user(id: UUID4, token: str = Depends(oauth2_scheme)):
    """
    get any user
    """
    auth_actions.get_current_user(token)
    user = user_actions.get_user(id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    return user


@router.get('/users', response_model=List[User], tags=['user'])
def get_users(skip: int = 0,
              limit: int = 100,
              token: str = Depends(oauth2_scheme)):
    """
    get many users
    """
    auth_actions.get_current_user(token)
    users = user_actions.get_users(skip, limit)
    return users


@router.put('/users', response_model=User, tags=['user'])
def update_user(token: str = Depends(oauth2_scheme),
                user_update: UserUpdate = Body(
                    ...,
                    example={
                        'name': 'Robert',
                        'email': 'bob@example.com',
                        'bio': 'logy #puns'
                    })):
    """
    update the current user
    """
    current_user = auth_actions.get_current_user(token)

    if current_user.email != user_update.email:
        if user_actions.get_user_by_email(user_update.email):
            raise HTTPException(status_code=422,
                                detail="This email is taken. Try another.")

    updated_user = user_actions.update_user(current_user.id, user_update)
    return updated_user


@router.delete('/users', tags=['user'])
def delete_user(token: str = Depends(oauth2_scheme)):
    """
    delete the current user
    """
    current_user = auth_actions.get_current_user(token)
    user_actions.delete_user(current_user)
    return current_user
