from datetime import datetime

from pydantic import BaseModel
from pydantic.types import StrictStr


class HealthcheckResponse(BaseModel):
    message: StrictStr
    version: StrictStr
    time: datetime
