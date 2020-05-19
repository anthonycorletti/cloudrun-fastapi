import json

from fastapi import APIRouter
from starlette.requests import Request

from actions.pubsub import pubsub_message_to_dict, send_pubsub_message
from config import logger
from schemas.push_message import PushMessage

router = APIRouter()


@router.post('/pubsub/publisher', tags=['pubsub'])
def publish():
    sample_data = json.dumps({'key': 'value'}).encode('utf8')
    response = send_pubsub_message('apipub', sample_data)
    return response


@router.post('/pubsub/subscriber', tags=['pubsub'])
def subscribe(message: PushMessage, request: Request):
    logger.info(f'request headers: {request.headers}')
    logger.info(f'request as dict: {dict(request)}')
    data = pubsub_message_to_dict(message)
    logger.info(f'message received: {data}')
    return
