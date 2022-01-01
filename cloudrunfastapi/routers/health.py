import os
from datetime import datetime

from fastapi import APIRouter

from cloudrunfastapi.logger import logger
from cloudrunfastapi.schemas.health import HealthcheckResponse

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", response_model=HealthcheckResponse, tags=tags)
def healthcheck() -> HealthcheckResponse:
    message = "We're on the air."
    version = os.getenv("SHORT_SHA", "local")
    logger.info(message)
    return HealthcheckResponse(message=message, version=version, time=datetime.now())
