import logging
import aioredis

from fastapi import FastAPI

from .utils import CacheBase, make_address
from .redis import RedisCache
from .. import config

logger = logging.getLogger(__name__)


class Cache:
    cache_cls: CacheBase = None

    @classmethod
    async def incr(cls, key, value=1):
        await cls.cache_cls.incrby(key, value)

    @classmethod
    async def incrby(cls, key, value):
        await cls.cache_cls.incrby(key, value)

    @classmethod
    async def set(cls, key, value):
        await cls.cache_cls.set(key, value)

    @classmethod
    async def get(cls, key, encoding="utf-8"):
        return await cls.cache_cls.get(key, encoding=encoding)

    @classmethod
    def exists_cache(cls):
        return cls.cache_cls.cache is not None

    @classmethod
    def register(cls, cache):
        cls.cache_cls.cache = cache


if config.ENABLE_REDIS:
    Cache.cache_cls = RedisCache


def init_app(app: FastAPI):
    address = make_address()

    @app.on_event("startup")
    async def register_redis():
        logger.info("======  init redis =====")
        if not Cache.exists_cache():
            redis_pool = await aioredis.create_redis_pool(
                address,
                password=config.REDIS_PASSWORD,
                maxsize=config.REDIS_MAXSIZE,
                minsize=config.REDIS_MINSIZE)
            Cache.register(redis_pool)
