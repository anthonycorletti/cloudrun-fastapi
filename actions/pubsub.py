import ast
import base64
import json

from config import logger, project_id, publisher
from schemas.push_message import PushMessage


def pubsub_message_to_dict(push_message: PushMessage) -> dict:
    """
    takes in a message body from gcp pubsub as bytes and returns a dict
    """
    message = push_message.message
    message_data = message.get('data')
    if not message_data:
        return {}
    b64data = base64.b64decode(message_data).decode('utf8')
    return json.loads(b64data)


def send_pubsub_message(topic_name: str, data: bytes) -> bool:
    topic = f'projects/{project_id}/topics/{topic_name}'
    publish_result = publisher.publish(topic, data)
    return publish_result.done()
