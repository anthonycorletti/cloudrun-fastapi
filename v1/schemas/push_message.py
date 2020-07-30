import base64
import json
from typing import Dict

from pydantic import BaseModel


class PushMessage(BaseModel):
    message: Dict
    subscription: str

    def data_dict(self) -> dict:
        message = self.message
        if not message.get("data"):
            return {}
        data = message.get("data")
        b64decoded_bytes = base64.b64decode(data)
        return json.loads(b64decoded_bytes.decode('utf8'))
