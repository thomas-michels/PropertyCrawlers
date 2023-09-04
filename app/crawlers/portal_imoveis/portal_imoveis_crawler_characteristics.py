from app.core.db import DBConnection
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.crawlers.base_crawler import Crawler


class PortalImoveisCrawlerCharacteristics(Crawler):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)
    
    def handle(self, message: EventSchema) -> bool:
        return super().handle(message)
