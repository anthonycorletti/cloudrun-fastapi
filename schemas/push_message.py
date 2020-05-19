from typing import Dict

from pydantic import BaseModel


class PushMessage(BaseModel):
    message: Dict
    subscription: str
