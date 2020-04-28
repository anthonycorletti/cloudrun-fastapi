from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from database import get_db

router = APIRouter()


@router.get('/pubsub/publisher', tags=['pubsub'])
def publish(db: Session = Depends(get_db)):
    pass


@router.post('/pubsub/subscriber', tags=['pubsub'])
async def subscribe(request: Request, db: Session = Depends(get_db)):
    print(dict(request))
    print(dict(request).keys())
    return
