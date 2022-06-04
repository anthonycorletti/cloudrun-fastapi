from datetime import datetime

from fastapi import APIRouter

from cloudrunfastapi import __version__
from cloudrunfastapi.logger import logger
from cloudrunfastapi.types import HealthcheckResponse

router = APIRouter()


@router.get("/healthcheck", response_model=HealthcheckResponse, tags=["health"])
def healthcheck() -> HealthcheckResponse:
    message = "We're on the air."
    logger.info(message)
    return HealthcheckResponse(
        message=message, version=__version__, time=datetime.now()
    )
