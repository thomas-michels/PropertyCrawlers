
from abc import abstractmethod, ABC
from app.core.db import DBConnection
from app.core.dependencies.worker.utils.event_schema import EventSchema


class Crawler(ABC):

    def __init__(self, conn: DBConnection) -> None:
        self.conn = conn

    @abstractmethod
    def handle(self, message: EventSchema) -> bool:
        ...
