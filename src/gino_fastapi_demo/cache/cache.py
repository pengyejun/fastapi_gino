import sys
import logging
from .. import config


def make_address() -> str:
    if config.ENABLE_REDIS:
        return f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"
    logging.error("invalid cache")
    sys.exit(-1)
