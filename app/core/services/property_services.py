from typing import List
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
    
    def set_updating(self, value: int) -> bool:
        self.__redis_conn.conn.setex(name="is_updating", value=value, time=3000)

    def is_updating(self) -> bool:
        return bool(self.__redis_conn.conn.get("is_updating"))

    def search_all_actived_properties(self) -> List[str]:
        query = """
        SELECT
            DISTINCT property_url,
            c."name" AS company
        FROM
            public.properties p
        INNER JOIN public.companies c ON
            p.company_id = c.id
        WHERE
            is_active IS TRUE;
        """

        self.__conn.execute(sql_statement=query)
        results = self.__conn.fetch(True)

        properties = []

        if results:
            for result in results:
                cached_on_redis = self.__redis_conn.conn.get(result["property_url"])

                if not cached_on_redis:
                    properties.append({
                        "property_url": result["property_url"],
                        "company": result["company"],
                    })

        return properties
