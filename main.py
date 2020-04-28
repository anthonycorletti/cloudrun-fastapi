import os

from fastapi import FastAPI

from routers import auth, default, item, pubsub, user

os.environ['TZ'] = 'UTC'
title_detail = os.getenv('PROJECT_ID', 'Local')
version = os.getenv('SHORT_SHA', 'local')

api = FastAPI(title=f"CloudRun FastAPI: {title_detail}", version=version)

api.include_router(default.router)
api.include_router(auth.router)
api.include_router(user.router)
api.include_router(item.router)
api.include_router(pubsub.router)
