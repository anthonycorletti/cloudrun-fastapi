from fastapi import APIRouter

from config import get_logger

logger = get_logger()
router = APIRouter()


@router.get('/health', tags=['default'])
def health():
    message = 'alive and kicking'
    logger.info(message)
    return {'message': message}
