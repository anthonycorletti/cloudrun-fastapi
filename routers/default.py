from fastapi import APIRouter

from config import get_logger

logger = get_logger()
router = APIRouter()


@router.get('/healthcheck', tags=['default'])
def healthcheck():
    message = 'alive and kicking'
    logger.debug(message)
    return {'message': message}
