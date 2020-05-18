import logging
import aioredis
from fastapi import FastAPI
from .. import config
from .cache import make_address, Cache

logger = logging.getLogger(__name__)


def init_app(app: FastAPI):
    address = make_address()

    @app.on_event("startup")
    async def register_redis():
        logger.info("======  init redis =====")
        if Cache.cache is None:
            redis_pool = await aioredis.create_redis_pool(
                address,
                password=config.REDIS_PASSWORD,
                maxsize=config.REDIS_MAXSIZE,
                minsize=config.REDIS_MINSIZE)
            Cache.cache = redis_pool
