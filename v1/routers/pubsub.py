import json

from fastapi import APIRouter

from v1.schemas.push_message import PushMessage
from v1.services.pubsub import PubsubService

router = APIRouter()
ps_service = PubsubService()


@router.post("/pubsub/publisher", tags=["pubsub"])
def publish():
    return ps_service.send_message("apipub",
                                   json.dumps({
                                       "key": "value"
                                   }).encode("utf8"))


@router.post("/pubsub/subscriber", tags=["pubsub"])
def subscribe(message: PushMessage):
    return message.data_dict()
