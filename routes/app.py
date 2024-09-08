from contextlib import asynccontextmanager
from math import ceil

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, status, Request, Response

from database import Base, engine
from fastapi_limiter import FastAPILimiter
from env_config import config

from . import todo, users


async  def service_name_identifier(request: Request):
    service = request.headers.get("Service-Name")
    return service

async def custom_callback(request: Request, response: Response, pexpire: int):
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Too many requests. Retry after {expire} seconds",
        headers={
            "Retry-After": str(expire)
        }
    )

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(config.REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(
        redis=redis_connection,
        identifier=service_name_identifier,
        http_callback=custom_callback
    )
    yield await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(todo.router, prefix="/todo", tags=["Todo List"])
