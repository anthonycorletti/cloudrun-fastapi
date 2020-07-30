import os
from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", tags=["public"])
def healthcheck():
    """
    going to the doctor
    """
    message = "alive and kicking"
    version = os.getenv("SHORT_SHA", "local")
    response = {
        "message": message,
        "version": version,
        "time": datetime.utcnow()
    }
    return response
