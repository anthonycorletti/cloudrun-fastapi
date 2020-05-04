import ast
import base64
import json

from config import logger, project_id, publisher
from schemas.push_message import PushMessage


def pubsub_message_to_dict(message: PushMessage) -> dict:
    """
    takes in a message body from gcp pubsub as bytes and returns a dict
    """
    data = json.loads(message.json())
    message = data.get('message')
    b64data = base64.b64decode(message.get('data', '')).decode('utf8')
    try:
        data_dict = json.loads(b64data)
    except Exception as e:
        msg = f'b64data {b64data} loading errored with {e}'
        logger.exception(msg)
        data_dict = ast.literal_eval(b64data)
    return data_dict


def send_pubsub_message(topic_name: str, data: bytes) -> bool:
    topic = f'projects/{project_id}/topics/{topic_name}'
    publish_result = publisher.publish(topic, data)
    return publish_result.done()
