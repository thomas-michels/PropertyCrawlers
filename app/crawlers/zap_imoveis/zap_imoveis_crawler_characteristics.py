from app.core.db import DBConnection
from app.core.dependencies.redis_client import RedisClient
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.crawlers.base_crawler import Crawler


class ZapImoveisCrawlerCharacteristics(Crawler):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
    
    def handle(self, message: EventSchema) -> bool:
        # _logger.info(f"New property: {raw_property.property_url}")
        return super().handle(message)
