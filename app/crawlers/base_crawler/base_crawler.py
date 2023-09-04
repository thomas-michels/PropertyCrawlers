
from abc import abstractmethod, ABC
from app.core.db import DBConnection
from app.core.dependencies.redis_client import RedisClient
from app.core.dependencies.worker.utils.event_schema import EventSchema


class Crawler(ABC):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        self.conn = conn
        self.redis_conn = redis_conn

    @abstractmethod
    def handle(self, message: EventSchema) -> bool:
        ...
