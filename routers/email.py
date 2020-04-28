from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter()


@router('/send_email', tags=['email'])
def send_email(db: Session = Depends(get_db)):
    pass
