import os

from fastapi import FastAPI

from config import get_logger
from routers import auth, default, item, user

logger = get_logger()

title_detail = os.getenv('PROJECT_ID', 'Local')
version = os.getenv('SHORT_SHA', 'local')

api = FastAPI(title=f"CloudRun FastAPI: {title_detail}", version=version)

api.include_router(default.router)
api.include_router(item.router)
api.include_router(user.router)
api.include_router(auth.router)
