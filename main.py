import os

from fastapi import FastAPI

from v1.routers import auth, health, item, user

os.environ["TZ"] = "UTC"
title_detail = os.getenv("PROJECT_ID", "Local")
version = os.getenv("SHORT_SHA", "local")

api = FastAPI(title=f"CloudRun FastAPI: {title_detail}", version=version)

# /
api.include_router(health.router)

# /v1
api_v1_prefix = "/v1"
api.include_router(auth.router, prefix=api_v1_prefix)
api.include_router(user.router, prefix=api_v1_prefix)
api.include_router(item.router, prefix=api_v1_prefix)
