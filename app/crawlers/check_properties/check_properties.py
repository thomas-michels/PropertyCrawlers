from app.core.db import DBConnection
from app.core.configs import get_environment, get_logger
from app.core.dependencies.redis_client import RedisClient
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.core.dependencies.worker.producer import KombuProducer
from app.core.dependencies import RedisClient
from app.core.services import PropertyServices
from app.crawlers.base_crawler import Crawler
from uuid import uuid4
from datetime import datetime

_env = get_environment()
_logger = get_logger(__name__)


class CheckProperties(Crawler):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)

    def handle(self, message: EventSchema) -> bool:
        _logger.info("Checking properties")
        services = PropertyServices(conn=self.conn, redis_conn=self.redis_conn)
        if services.is_updating():
            _logger.info("Properties checked")
            return True

        services.set_updating(value=1)

        properties = services.search_all_actived_properties()
        _logger.info(f"Properties: {len(properties)}")

        if properties:
            for property in properties:
                if property["company"] == "portal_imoveis":
                    sent_to = _env.PORTAL_IMOVEIS_IN_CHANNEL

                else:
                    sent_to = _env.ZAP_IMOVEIS_IN_CHANNEL

                event = EventSchema(
                    id=str(uuid4()),
                    origin="CHECK_PROPERTIES",
                    sent_to=sent_to,
                    payload=property,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )

                KombuProducer.send_messages(conn=self.conn, message=event)

        _logger.info("Properties checked")
        return True
