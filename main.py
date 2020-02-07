import os

from fastapi import FastAPI

import config

logger = config.setup_logger()

title_detail = os.getenv('PROJECT_ID', 'Local')
version = os.getenv('SHORT_SHA', 'local')

api = FastAPI(title=f"CloudRun FastAPI: {title_detail}", version=version)


@api.get('/health')
def health():
    message = 'alive and kicking'
    logger.info(message)
    return {'message': message}
