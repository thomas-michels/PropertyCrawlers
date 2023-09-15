from app.core.dependencies import RedisClient
from app.core.db import DBConnection
from app.core.configs import get_environment, get_logger

_env = get_environment()
_logger = get_logger(__name__)


class PropertyServices:

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        self.__conn = conn
        self.__redis_conn = redis_conn

    def save(self, url: str) -> bool:

        timed_cache = _env.TIMED_CACHE * 60

        self.__redis_conn.conn.setex(name=url, value=1, time=timed_cache)
        _logger.info(f"Caching {url}")

        return True

    def search_by_url(self, url: str) -> bool:
        return bool(self.__redis_conn.conn.get(url))
