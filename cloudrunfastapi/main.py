import os
import time
from typing import Any, Callable

from fastapi import FastAPI, Request

from cloudrunfastapi.routers import auth, health, item, user

os.environ["TZ"] = "UTC"
title_detail = os.getenv("PROJECT_ID", "Local")
version = os.getenv("SHORT_SHA", "local")

#
#   create the api
#
api = FastAPI(title=f"CloudRun FastAPI: {title_detail}", version=version)


#
#   middleware
#
@api.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


#
#   set routers
#
api.include_router(health.router)
api.include_router(auth.router)
api.include_router(user.router)
api.include_router(item.router)
