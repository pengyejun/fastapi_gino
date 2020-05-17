import logging
import aioredis
from aioredis import Redis
from fastapi import FastAPI
from .. import config
from .cache import make_address

redis_pool: Redis = None


def init_app(app: FastAPI):
    address = make_address()

    @app.on_event("startup")
    async def register_redis():
        global redis_pool
        if redis_pool is None:
            redis_pool = await aioredis.create_redis_pool(
                address,
                password=config.REDIS_PASSWORD,
                maxsize=config.REDIS_MAXSIZE,
                minsize=config.REDIS_MINSIZE)
            logging.debug("======  init redis =====")
