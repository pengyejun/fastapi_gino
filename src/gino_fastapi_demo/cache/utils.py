import abc
import sys
import logging

from .. import config


class CacheBase(abc.ABC):
    cache = None

    @classmethod
    @abc.abstractmethod
    async def incr(cls, key, value=1):
        pass

    @classmethod
    @abc.abstractmethod
    async def incrby(cls, key, value):
        pass

    @classmethod
    @abc.abstractmethod
    async def set(cls, key, value):
        pass

    @classmethod
    @abc.abstractmethod
    async def get(cls, key, encoding='utf-8'):
        pass


def make_address() -> str:
    if config.ENABLE_REDIS:
        return f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"
    logging.error("invalid cache")
    sys.exit(-1)
