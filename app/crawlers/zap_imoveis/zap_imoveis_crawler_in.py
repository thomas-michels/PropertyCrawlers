from app.core.db import DBConnection
from app.core.dependencies.redis_client import RedisClient
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.core.services import PropertyServices
from app.crawlers.base_crawler import Crawler
from app.core.dependencies.worker import KombuProducer
from app.core.configs import get_environment
from datetime import datetime

_env = get_environment()


class ZapImoveisCrawlerIn(Crawler):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)

        self.__property_services = PropertyServices(
            conn=self.conn,
            redis_conn=self.redis_conn
        )
    
    def handle(self, message: EventSchema) -> bool:
        url = message.payload["property_url"]

        if self.__property_services.search_by_url(url=url):
            return True

        else:
            self.__property_services.save(url=url)

        new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.ZAP_IMOVEIS_CHARACTERISTICS_CHANNEL,
                payload=message.payload,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        return KombuProducer.send_messages(conn=self.conn, message=new_message)
