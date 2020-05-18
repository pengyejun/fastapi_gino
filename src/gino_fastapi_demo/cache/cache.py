import sys
import abc
import logging
from aioredis import Redis
from .. import config


def make_address() -> str:
    if config.ENABLE_REDIS:
        return f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"
    logging.error("invalid cache")
    sys.exit(-1)


class CacheBase(abc.ABC):
    cache = None

    @classmethod
    @abc.abstractmethod
    async def incr(cls, key, value=1):
        pass

    @classmethod
    @abc.abstractmethod
    async def set(cls, key, value):
        pass

    @classmethod
    @abc.abstractmethod
    async def get(cls, key):
        pass


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


Cache: CacheBase = None

if config.ENABLE_REDIS:
    Cache = RedisCache
