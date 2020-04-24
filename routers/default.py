from fastapi import APIRouter

from config import logger

router = APIRouter()


@router.get('/healthcheck', tags=['default'])
def healthcheck():
    detail = 'alive and kicking'
    logger.info(detail)
    return {'detail': detail}
