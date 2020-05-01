from fastapi import APIRouter
from starlette.requests import Request

from config import logger

router = APIRouter()


@router.get('/pubsub/publisher', tags=['pubsub'])
def publish():
    return


@router.post('/pubsub/subscriber', tags=['pubsub'])
def subscribe(request: Request):
    logger.debug(dict(request))
    logger.debug(dict(request).keys())
    return
