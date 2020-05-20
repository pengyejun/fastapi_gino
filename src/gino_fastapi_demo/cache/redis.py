import logging
from aioredis import Redis
from .utils import CacheBase

logger = logging.getLogger(__name__)


class RedisCache(CacheBase):
    cache: Redis = None

    @classmethod
    async def incr(cls, key, value=1):
        await cls.incrby(key, value)

    @classmethod
    async def incrby(cls, key, value):
        await cls.cache.incrby(key, value)

    @classmethod
    async def set(cls, key, value):
        await cls.cache.set(key, value)

    @classmethod
    async def get(cls, key, encoding="utf-8"):
        return await cls.cache.get(key, encoding=encoding)
